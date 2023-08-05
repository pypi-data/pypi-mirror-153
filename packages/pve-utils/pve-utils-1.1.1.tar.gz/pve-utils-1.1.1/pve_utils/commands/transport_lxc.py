import sys

import click
from proxmoxer import ProxmoxAPI

from pve_utils.config import settings
from pve_utils.resources import ProxmoxNode


@click.command()
@click.option(
    "-N",
    "--node-name",
    default=settings.PROXMOX_NODE,
    required=False,
    type=str,
    help="Name of Proxmox Node.",
)
@click.option(
    "-H",
    "--host-name",
    default=settings.CT_HOST,
    required=False,
    type=str,
    help="Name of CT.",
)
@click.argument("host_path")
@click.argument("container_path")
def transport_lxc(
    node_name: str,
    host_name: str,
    host_path: str,
    container_path: str,
):
    """
    Upload files from HOST to CT
    command provides like a string
    (shell_lxc -N ktiib -H new1.rsue.ru host_path container_path)
    other settings provides with env
    """

    conn = ProxmoxAPI(
        settings.PROXMOX_URL,
        port=settings.PROXMOX_PORT,
        user=settings.PROXMOX_USER,
        password=settings.PROXMOX_PASSWORD,
        verify_ssl=settings.PROXMOX_VERIFY_SSL,
    )

    node_worker = ProxmoxNode(conn, node_name)
    ct = node_worker.get_lxc(host_name, create=False)
    print(host_path, container_path)
    if not ct:
        sys.exit(1)

    ct.upload(host_path, container_path)


if __name__ == "__main__":
    transport_lxc()
