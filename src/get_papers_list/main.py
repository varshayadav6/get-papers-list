# get_papers_list/main.py
from get_papers_list import utils


from get_papers_list import parser

from get_papers_list import pubmed_client


import typer

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    file: str = typer.Option(None, "--file", "-f", help="CSV filename to save results"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
):
    """
    Fetch PubMed articles with non-academic authors from pharma/biotech companies.
    """
    if debug:
        typer.echo(f"Query: {query}")
        typer.echo("Debug mode is ON.")

    # You will fetch and process data here later
    ids = pubmed_client.fetch_pubmed_ids(query, max_results=10)
    typer.echo(f"Found {len(ids)} paper IDs.")
    
    xml_data = pubmed_client.fetch_pubmed_details(ids)
    typer.echo("Fetched paper details in XML format.")
    
    papers = parser.parse_pubmed_xml(xml_data)
    typer.echo(f"{len(papers)} papers with non-academic authors found.")
    
    if file:
        typer.echo(f"Saving results to: {file}")
        utils.save_to_csv(papers, file)
    
    else:
        import pprint
        pprint.pprint(papers)


if __name__ == "__main__":
    app()
