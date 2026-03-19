# pyads-standalone

`pyads-standalone` serve per usare `pyads` su Windows anche se TwinCAT non e
installato sul PC client.

In pratica:

- installi questo pacchetto
- continui a scrivere `import pyads`
- su Windows viene usata una `TcAdsDll.dll` inclusa nel wheel

Se TwinCAT e gia installato e `TWINCAT3DIR` e presente, il pacchetto non forza
la DLL bundleata e lascia lavorare la DLL di TwinCAT.

## Risposta breve alla domanda "e tutto standalone?"

Per chi usa il pacchetto:

- si, questo deve diventare completamente standalone
- l utente finale deve solo fare `pip install ...`
- non deve installare TwinCAT
- non deve installare Ninja
- non deve installare Meson
- non deve installare Visual Studio per usare il wheel gia pronto

Per chi crea il wheel:

- Python puo scaricare da solo i tool Python di build
- ma la DLL Windows resta una libreria C/C++, quindi da qualche parte serve
  comunque un compilatore Windows

Quindi il modello giusto e questo:

- gli utenti finali installano un wheel gia compilato
- la compilazione viene fatta una volta sola in CI su Windows
- poi tutti gli utenti usano solo il wheel, senza tool extra

## Quando ti serve

Usa questo pacchetto se:

- hai un PC Windows 64 bit
- vuoi usare `pyads`
- non vuoi installare TwinCAT sul PC client

## Cosa non cambia

Questo pacchetto toglie la dipendenza da TwinCAT sul PC client, ma non elimina
le regole normali di ADS.

Restano comunque necessari:

- un PLC o target Beckhoff/TwinCAT raggiungibile in rete
- un AMS Net ID del target
- una route AMS corretta tra il tuo PC e il target

## Requisiti per chi lo usa

- Windows 64 bit
- Python compatibile con `pyads` 3.5.x
- accesso di rete al PLC o al target ADS

## Installazione

Se il pacchetto e pubblicato su PyPI:

```bash
pip install pyads-standalone
```

Se hai gia il wheel locale:

```bash
pip install pyads_standalone-0.1.0-py3-none-win_amd64.whl
```

Questo pacchetto installa anche `pyads` come dipendenza.

Per l utente finale, qui finisce tutto: non servono altri tool.

## Uso veloce

Se hai gia una route AMS funzionante, il codice Python resta quello normale di
`pyads`.

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

## Primo uso senza TwinCAT sul PC

Se sul PC client non hai TwinCAT, il caso piu sicuro e questo:

1. scegli un AMS Net ID locale per il tuo PC, per esempio `192.168.0.50.1.1`
2. apri la porta ADS
3. imposti l AMS Net ID locale
4. aggiungi la route locale verso il PLC
5. ti connetti al PLC

Esempio:

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

## Route AMS: cosa devi fare davvero

Per comunicare via ADS serve che il target accetti il tuo client.

Quindi devi avere almeno una di queste due situazioni:

- la route dal target verso il tuo PC e gia configurata
- la crei tu via codice con `pyads.add_route_to_plc(...)`

Esempio di creazione route sul PLC:

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

Se non esiste una route valida, il pacchetto e installato correttamente ma la
connessione ADS fallira comunque.

## Se TwinCAT e gia installato

Non devi fare nulla di speciale.

Puoi installare comunque `pyads-standalone`, ma se `TWINCAT3DIR` e presente il
package non sostituisce la DLL di TwinCAT e lascia il comportamento standard.

## Errori comuni

### `TcAdsDll.dll` non trovata

Controlla che:

- il pacchetto sia installato nello stesso ambiente Python da cui esegui lo script
- tu stia usando Windows 64 bit
- l installazione non sia stata fatta in modo parziale

### Timeout o errore ADS quando apri la connessione

Di solito significa che:

- IP o AMS Net ID del PLC sono sbagliati
- manca la route AMS sul PLC o sul target
- firewall o rete bloccano la comunicazione

### Il codice funziona su Linux ma non su Windows

Controlla soprattutto:

- AMS Net ID locale impostato
- route verso il target
- route di ritorno dal target verso il PC

## Cosa e stato testato

Testati in questo repository:

- bootstrap Python del package
- patch delle funzioni `pyads` che su Windows erano bloccate
- metadata packaging Python

Limite importante:

- non ho potuto compilare e provare davvero la DLL Windows in questo ambiente
  Linux
- la validazione reale della build Windows e demandata alla CI Windows in
  `.github/workflows/ci.yml`

Quindi: la parte Python e stata testata, la parte finale Windows va ancora
confermata con una build su Windows.

## Cosa devi fare adesso

Se vuoi usare il progetto davvero, i prossimi passi sono questi:

1. eseguire la build o la CI su una macchina Windows
2. verificare che venga prodotto il wheel `win_amd64`
3. installare quel wheel in una venv Windows pulita
4. fare una prova reale contro un PLC o contro il testserver
5. pubblicare il wheel su PyPI o sul tuo indice interno

## Per chi deve costruire il wheel

### Caso consigliato: non compilare in locale

Il modo migliore e questo:

1. fai push del repository
2. lanci la GitHub Actions su Windows
3. scarichi il wheel prodotto
4. pubblichi quel wheel

In questo caso sul PC dell utente finale non serve nulla oltre a Python.

### Caso locale: vuoi compilare tu il wheel su Windows

Serve solo questo:

- Python
- un compilatore C++ per Windows

Nel caso piu semplice:

- Visual Studio 2022 Build Tools o Visual Studio con workload C++

Gli altri tool Python vengono scaricati automaticamente dal build.

Comando piu semplice:

```bash
python scripts/build_wheel.py
```

Questo script:

- crea una venv locale `.build-venv`
- installa `build`
- lascia che il sistema di build scarichi da solo `setuptools`, `wheel`,
  `meson` e `ninja`
- compila i sorgenti Beckhoff ADS presenti in `vendor/ADS`
- crea il wheel con dentro `TcAdsDll.dll`

Quindi:

- `meson` e `ninja` non devi installarli tu a mano
- il compilatore C++ invece non puo essere evitato se vuoi compilare la DLL

### Se vuoi zero dipendenze locali davvero

Allora non devi compilare in locale.

Devi:

1. usare la CI Windows per produrre il wheel
2. distribuire solo wheel gia compilati
3. far installare agli utenti solo quel wheel

## Licenze

Questo repository include i sorgenti Beckhoff ADS in `vendor/ADS`.

Dettagli:

- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [LICENSE](LICENSE)
