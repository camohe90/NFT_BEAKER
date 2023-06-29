from pathlib import Path

from beaker import *
from pyteal import *

from utils import build

app = Application("HelloWorld")


@app.external
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.external
def mint(name: abi.String, unit_name: abi.String, *, output: abi.String) -> Expr:
     return InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: name.get(),
                TxnField.config_asset_unit_name: unit_name.get(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_url: Bytes("https://gateway.pinata.cloud/ipfs/QmcZyZ8KXSJomNBHS9QK4zMqH11dGZzQm3ye7Rtk8Qofys"),
                TxnField.config_asset_total: Int(1),
            }
     )

if __name__ == "__main__":
    root_path = Path(__file__).parent
    build(root_path / "artifacts", app)
