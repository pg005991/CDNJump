"""
CLI para CDN-Jump

Este módulo proporciona un menú interactivo que recoge las funcionalidades
del script Bash original:
  - Obtención de registros DNS.
  - Historial de resoluciones y certificados (utilizando la API de VirusTotal).
  - Búsqueda en Censys (para certificados y hosts).
  - Validaciones de contenido HTTP/HTTPS (por líneas y por similitud).
  - Detección de CDNs mediante búsquedas PTR, whois y análisis de cabeceras.
  
Se ofrecen cuatro modos de ejecución:
  1. Modo Básico: Escaneo estándar.
  2. Modo Intensivo: Escaneo intensivo (incluye búsqueda de AS owner y paginación intensiva).
  3. Modo Censys: Incorpora búsqueda en la API de Censys.
  4. Modo Todo: Combina los modos Intensivo y Censys.
  
El menú interactivo permite, además, elegir entre analizar un dominio único o
procesar un fichero con varios dominios.
"""

import click
from main import main_logic

@click.command()
@click.option(
    '--interactive',
    is_flag=True,
    default=False,
    help="Ejecutar en modo interactivo con menú."
)
@click.option(
    '-d', '--domain',
    type=str,
    help="Dominio a analizar (ej: ejemplo.com)."
)
@click.option(
    '-f', '--file',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Fichero con lista de dominios a analizar."
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=False,
    help="Activar modo verbose."
)
def scan(interactive, domain, file, verbose):
    """
    Escanea dominios utilizando las funcionalidades integradas: \n
      - Consultas DNS y extracción de historial de resoluciones/certificados con VirusTotal. \n
      - Búsqueda en Censys para certificados e IPs. \n
      - Validaciones de contenido HTTP/HTTPS. \n
      - Detección de CDNs. \n\n

    Se pueden ejecutar en los siguientes modos: \n
      1. Modo Básico: Escaneo estándar. \n
      2. Modo Intensivo: Incluye análisis intensivo (p.ej., AS owner). \n
      3. Modo Censys: Incorpora búsqueda en la API de Censys. \n
      4. Modo Todo: Combina las opciones Intensivo y Censys.\n\n
    """
    # Inicialización de las banderas de modo.
    intensive = False
    censys = False

    # Si se activa el modo interactivo, se muestra el menú.
    if interactive:
        click.echo("\n=== CDN-Jump: Menú de Escaneo ===")
        click.echo("Seleccione el modo de escaneo:")
        click.echo("  1. Modo Básico")
        click.echo("  2. Modo Intensivo")
        click.echo("  3. Modo Censys")
        click.echo("  4. Modo Todo (Intensivo + Censys)")
        mode = click.prompt("Ingrese el número del modo", type=int)
        
        if mode == 1:
            intensive = False
            censys = False
        elif mode == 2:
            intensive = True
            censys = False
        elif mode == 3:
            intensive = False
            censys = True
        elif mode == 4:
            intensive = True
            censys = True
        else:
            click.echo("Opción no válida. Abortando.")
            raise click.Abort()
        
        click.echo("\nSeleccione el método de entrada:")
        click.echo("  1. Dominio único")
        click.echo("  2. Fichero con dominios")
        entrada = click.prompt("Ingrese el número de entrada", type=int)
        
        if entrada == 1:
            domain = click.prompt("Introduzca el dominio", type=str)
        elif entrada == 2:
            file = click.prompt(
                "Introduzca la ruta del fichero con dominios",
                type=click.Path(exists=True, dir_okay=False, readable=True)
            )
        else:
            click.echo("Opción no válida. Abortando.")
            raise click.Abort()
    
    # Validación: se debe proporcionar un dominio o un fichero.
    if not domain and not file:
        click.echo("Error: Debe proporcionar un dominio (-d) o un fichero (-f).")
        raise click.Abort()

    if verbose:
        click.echo("\nOpciones seleccionadas:")
        if domain:
            click.echo(f"  - Dominio: {domain}")
        if file:
            click.echo(f"  - Fichero: {file}")
        click.echo(f"  - Modo Intensivo: {'Sí' if intensive else 'No'}")
        click.echo(f"  - Modo Censys: {'Sí' if censys else 'No'}\n")
    
    # Se invoca la función principal que orquesta el análisis, pasando los parámetros.
    try:
        main_logic(
            domain=domain,
            file=file,
            intensive=intensive,
            censys=censys,
            verbose=verbose
        )
    except Exception as e:
        click.echo(f"Se ha producido un error durante la ejecución: {e}")
        raise click.Abort()

if __name__ == '__main__':
    scan()

