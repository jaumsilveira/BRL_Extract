from datetime import datetime, timedelta
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

username = "username"
password = "password"

#### Sharepoint ####
site_url = "https://g4fcombr.sharepoint.com"
folder_url = "/Documentos/BI/BRL"
authcookie = Office365(site_url, username=username, password=password).GetCookies()
site = Site(site_url, version=Version.v365, authcookie=authcookie)
folder = site.Folder(folder_url)

#### Sharepoint ####

today = datetime.now()


def format_date(date):
    return date.strftime('%d/%m/%Y')


def upload(file):
    file_path = f"C:/Users/joaop/Downloads/BRL/{file}"
    try:
        with open(file_path, "rb") as file_data:
            folder.upload_file(file_data, file)
            response_data = {"status": "success", "message": f"{file} uploaded successfully"}
    except Exception as e:
        response_data = {"status": "error", "message": f"Failed to upload {file}: {str(e)}"}
    # Convert the response data to JSON
    response_json = json.dumps(response_data)
    # Print or return the JSON response
    print(response_json)


def downloadUpload(file):
    i = 1
    file_paths = []

    # today = datetime.now()
    # d30 = today - timedelta(days=30)
    # d60 = today - timedelta(days=60)
    # d90 = today - timedelta(days=90)
    #
    # date_ranges = [
    #     (d30, today),
    #     (d60, d30 - timedelta(days=1)),
    #     (d90, d60 - timedelta(days=1))
    # ]

    date_ranges = [
        (timedelta(days=30 * i), timedelta(days=30 * (i - 1)) + timedelta(days=1) if i > 1 else None) for i in
        range(1, 4)  # se i=1 end_Date = null
    ]

    for date_range in date_ranges:
        path = f"C:/Users/joaop/Downloads/BRL/{i}{file}.xls"
        start_date, end_date = date_range
        time.sleep(1)
        page.frame_locator("#iframePaginas").locator("#ctl00_cphContent_txtDataIni").fill(
            format_date(today - start_date))
        time.sleep(1)
        page.frame_locator("#iframePaginas").locator("#ctl00_cphContent_txtDataFin").fill(
            format_date(today - end_date) if end_date else format_date(today))  # se end_date for null retorna hoje
        with page.expect_download() as download_info:
            page.frame_locator("#iframePaginas").get_by_role("button", name="Pesquisar").click()
        download = download_info.value
        file_paths.append(download.path().as_posix())
        download.save_as(path)
        page.evaluate('window.scrollTo(0, 1000);')
        page.frame_locator("#iframePaginas").get_by_label("Aviso").get_by_role("button").click()
        i += 1
    dataframes = [pd.read_excel(file_path) for file_path in file_paths]
    combined_dataframe = pd.concat(dataframes, ignore_index=True)
    combined_dataframe.to_excel(f'C:/Users/joaop/Downloads/BRL/{file}.xlsx', index=False)
    upload(f"{file}.xlsx")
    print('Ok')


def check_labels(page, labels):
    for label in labels:
        page.frame_locator("#iframePaginas").get_by_label(label, exact=True).check()


def main(relatorio, file):
    page.evaluate('window.scrollTo(0, 0);')
    page.frame_locator("#iframePaginas").locator("#ctl00_cphContent_ddlDespesa").select_option(
        relatorio if relatorio not in ['P1', 'P2'] else 'P')
    page.frame_locator("#iframePaginas").get_by_label("Excel (.xls)").check()
    if relatorio == 'H':
        check_labels(page, [
            "Data/Hora da Solicitação", "Cidade/Estado/País", "Número da Solicitação",
            "Solicitante", "Viajante", "Motivo de Viagem", "Centro Custo de Débito",
            "Observação", "Hotel", "Localização", "Tipo de Apartamento",
            "Valor Total", "Quantidade de Diárias", "Status da(s) Aprovação(ões)"
        ])
    elif relatorio == 'AR':
        check_labels(page, ["Lançamentos"])
    elif relatorio == 'T':
        check_labels(page, [
            "Número da Solicitação", "Solicitante", "Viajante", "Motivo de Viagem",
            "Centro Custo de Débito", "Data/Hora da Solicitação", "Observação",
            "Status da(s) Aprovação(ões)", "Aeroporto de Origem", "Aeroporto de Destino",
            "Data / Hora Saída", "Data / Hora Chegada", "Quantidade de Conexões",
            "Provedor", "Bagagem", "Reembolso", "Alteração de voo", "Valor Total"
        ])
    elif relatorio == 'P1':
        page.frame_locator("#iframePaginas").locator("#ctl00_cphContent_ddlDespesa").select_option('P')
        check_labels(page, ["Realizado"])
    elif relatorio == 'P2':
        page.frame_locator("#iframePaginas").locator("#ctl00_cphContent_ddlDespesa").select_option('P')
        check_labels(page, ["Pendentes"])
    downloadUpload(file)


# Usage
# Assuming the `page` variable is already defined and refers to the webpage object.
with sync_playwright() as p:
    nav = p.chromium.launch(headless=False)
    page = nav.new_page()
    print('Start')

    ### LOGIN ###
    page.goto("https://www.argoit.com.br/brlcorporate/default.aspx?cliente=g4f")
    page.get_by_placeholder("Usuário").fill('username')
    page.get_by_placeholder("Senha").fill('password')
    page.get_by_role("button", name="Acessar").press("Enter")
    page.locator("a").filter(has_text="Relatórios").nth(1).click()
    main('H', 'Hospedagem')
    main('AR', 'AdiantamentoReembolso')
    main('T', 'PassagemAerea')
    main('P1', 'PagamentoRealizado')
    main('P2', 'PagamentoPendente')
