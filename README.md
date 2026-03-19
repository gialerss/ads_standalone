# pyads-standalone

`pyads-standalone` serve per usare `pyads` su Windows senza installare
TwinCAT.

In pratica:

- installi questo pacchetto
- continui a scrivere `import pyads`
- su Windows viene usata una `TcAdsDll.dll` inclusa nel wheel

## A chi serve

Questo pacchetto ti serve se:

- usi Windows 64 bit
- vuoi leggere o scrivere variabili ADS da Python
- non vuoi installare TwinCAT sul PC client

## Cosa ti serve davvero

Per usare questo pacchetto ti servono solo:

- Windows 64 bit
- Python
- accesso di rete al PLC o al dispositivo ADS
- IP del PLC
- AMS Net ID del PLC

Non ti servono:

- TwinCAT sul PC client
- Ninja
- Meson
- Visual Studio

## Cosa non cambia

Questo pacchetto toglie TwinCAT dal PC client, ma ADS continua a funzionare
come sempre.

Quindi restano comunque necessari:

- un PLC o un target ADS raggiungibile
- una route AMS corretta
- un AMS Net ID locale valido sul tuo PC

## Installazione

Se il pacchetto e pubblicato su PyPI:

```bash
pip install pyads-standalone
```

Se hai un wheel gia pronto:

```bash
pip install pyads_standalone-0.1.0-py3-none-win_amd64.whl
```

Dopo l installazione non devi fare altro.

## Come si usa

Il codice Python resta quello normale di `pyads`.

Import:

```python
import pyads
```

## Caso 1: hai gia una route AMS funzionante

Se il PLC ha gia una route valida verso il tuo PC, puoi usare direttamente
`pyads` come faresti su Linux.

Esempio:

```python
import pyads

PLC_IP = "192.168.0.10"
PLC_AMS = "192.168.0.10.1.1"

plc = pyads.Connection(PLC_AMS, pyads.PORT_TC3PLC1, PLC_IP)
plc.open()

value = plc.read_by_name("GVL.my_value")
print(value)

plc.close()
```

## Caso 2: non hai TwinCAT e devi partire da zero

Se sul PC non hai TwinCAT, il flusso tipico e questo:

1. scegli un AMS Net ID locale per il tuo PC
2. apri la porta ADS
3. imposti il tuo AMS Net ID locale
4. aggiungi la route verso il PLC
5. apri la connessione

Esempio completo:

```python
import pyads

LOCAL_AMS = "192.168.0.50.1.1"
PLC_IP = "192.168.0.10"
PLC_AMS = "192.168.0.10.1.1"

pyads.open_port()
pyads.set_local_address(LOCAL_AMS)
pyads.add_route(PLC_AMS, PLC_IP)

plc = pyads.Connection(PLC_AMS, pyads.PORT_TC3PLC1, PLC_IP)
plc.open()

print(plc.read_by_name("GVL.my_value"))

plc.close()
pyads.close_port()
```

## Se il PLC non conosce ancora il tuo PC

In questo caso devi creare la route anche sul PLC.

Puoi farlo via codice con `pyads.add_route_to_plc(...)`.

Esempio:

```python
import pyads

ok = pyads.add_route_to_plc(
    sending_net_id="192.168.0.50.1.1",
    adding_host_name="my-pc",
    ip_address="192.168.0.10",
    username="Administrator",
    password="1",
    route_name="my-pc",
    added_net_id="192.168.0.50.1.1",
)

print(ok)
```

Se questa route non esiste, il pacchetto e installato bene ma la connessione
ADS non funzionera.

## Ordine giusto per il primo test

Se vuoi provare la libreria da zero, fai cosi:

1. installa il pacchetto
2. verifica IP e AMS Net ID del PLC
3. scegli un AMS Net ID locale per il tuo PC
4. esegui `pyads.open_port()`
5. esegui `pyads.set_local_address(...)`
6. esegui `pyads.add_route(...)` oppure `pyads.add_route_to_plc(...)`
7. apri la connessione con `pyads.Connection(...)`
8. prova una `read_by_name(...)`

## Esempio minimo pronto da copiare

```python
import pyads

LOCAL_AMS = "192.168.0.50.1.1"
PLC_AMS = "192.168.0.10.1.1"
PLC_IP = "192.168.0.10"

pyads.open_port()
pyads.set_local_address(LOCAL_AMS)
pyads.add_route(PLC_AMS, PLC_IP)

plc = pyads.Connection(PLC_AMS, pyads.PORT_TC3PLC1, PLC_IP)
plc.open()

try:
    print(plc.read_by_name("GVL.my_value"))
finally:
    plc.close()
    pyads.close_port()
```

## Se TwinCAT e gia installato

Puoi installare comunque `pyads-standalone`.

Se sul PC e presente `TWINCAT3DIR`, il pacchetto non forza la DLL bundleata e
lascia il comportamento standard di TwinCAT.

## Errori comuni

### `TcAdsDll.dll` non trovata

Controlla che:

- stai usando lo stesso ambiente Python in cui hai installato il pacchetto
- stai usando Windows 64 bit
- il wheel e stato installato correttamente

### Timeout o errore ADS

Di solito significa:

- IP del PLC sbagliato
- AMS Net ID del PLC sbagliato
- AMS Net ID locale sbagliato
- route AMS mancante
- firewall o rete che bloccano la comunicazione

### Funziona su Linux ma non su Windows

Controlla soprattutto:

- AMS Net ID locale impostato sul PC
- route dal PC verso il PLC
- route dal PLC verso il PC

## Come capire se e installato bene

Questa prova deve funzionare:

```python
import pyads
print(pyads.__version__)
```

Se l import funziona, il pacchetto e installato.

Se poi anche la connessione ADS funziona, allora il wheel bundleato sta
lavorando correttamente.

## Dove prendere il wheel

Se non usi PyPI, puoi distribuire direttamente il file `.whl` Windows gia
compilato.

Questo e il formato corretto:

```text
pyads_standalone-0.1.0-py3-none-win_amd64.whl
```

## Per chi mantiene il progetto

Per creare il wheel Windows:

- usa AppVeyor oppure una macchina Windows
- il comando locale completo e `python scripts/validate_windows.py`

Questo comando:

- esegue i test Python
- compila `TcAdsDll.dll`
- crea il wheel
- installa il wheel in una venv pulita
- esegue uno smoke test finale

## Licenze

Questo repository include i sorgenti Beckhoff ADS in `vendor/ADS`.

Dettagli:

- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [LICENSE](LICENSE)
