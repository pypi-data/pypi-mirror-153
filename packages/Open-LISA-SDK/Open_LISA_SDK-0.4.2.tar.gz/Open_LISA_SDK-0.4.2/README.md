# [DEPRECATED] Electronic Instrument Adapter SDK

This SDK provides an interface to interact with the [Electronic Instrument Adapter server](https://github.com/aalvarezwindey/electronic-instrument-adapter/). The server must be integrated with the instruments of interest and running in a known IP and port in order to be able to connect via this SDK.

## Installation

```
pip install electronic-instrument-adapter-sdk
```

## Examples

### List available and registered instruments

```python
import electronic_instrument_adapter_sdk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, help="server host", default="127.0.0.1")
parser.add_argument("--port", type=int, help="server port", default=8080)
args = parser.parse_args()

# Connect with server running on localhost and port 8080
sdk = electronic_instrument_adapter_sdk.EIA(args.host, args.port)

# List instruments
print(sdk.list_instruments())
```

### Check specific instrument commands

This snippet list all available commands for the first instrument returned by the server.

```python
import electronic_instrument_adapter_sdk

sdk = electronic_instrument_adapter_sdk.EIA("127.0.0.1", 8080)

instruments = sdk.list_instruments()

if len(instruments) != 0:
  instrument = instruments[0]

  commands = instrument.available_commands()
  for c in commands:
    print(c)
else:
  print("no instruments available")
```

### Validate command

The instruments commands that are configured in the server side have a specefic syntax. This command let you check that if some command you are trying to send to an instrument is valid. This is a recommended practice in order to prevent sending invalid commands to the instruments.

```python
import electronic_instrument_adapter_sdk

sdk = electronic_instrument_adapter_sdk.EIA("127.0.0.1", 8080)

instruments = sdk.list_instruments()

if len(instruments) != 0:
  instrument = instruments[0]

  instrument.validate_command("unexisting command")
  instrument.validate_command("set_waveform_encoding_ascii")
  instrument.validate_command("set_trigger_level 10 20")
  instrument.validate_command("set_trigger_level ASCII")
  instrument.validate_command("set_trigger_level 3.4")
else:
  print("no instruments available")
```

### Sending commands

This advance usage of the SDK shows how to plot what is shown in channel 1 of a Tektronix TDS1002B Oscilloscope. Note the example assumes that the instrument (with ID `USB0::0x0699::0x0363::C107676::INSTR`) is configured on the server side with this specific commands:

```python
import electronic_instrument_adapter_sdk
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, help="server host", default="127.0.0.1")
parser.add_argument("--port", type=int, help="server port", default=8080)
args = parser.parse_args()

sdk = electronic_instrument_adapter_sdk.EIA(args.host, args.port)

instruments = sdk.list_instruments()
osc_tds1002b = None
for i in instruments:
  if i.ID == "USB0::0x0699::0x0363::C107676::INSTR":
    osc_tds1002b = i

if osc_tds1002b:
  osc_tds1002b.send("set_waveform_source_ch1")
  osc_tds1002b.send("set_waveform_bytes_width_1")
  osc_tds1002b.send("set_waveform_encoding_rpbinary")
  Volts = np.empty(0)
  ymult = float(osc_tds1002b.send("get_waveform_vertical_scale_factor"))
  yzero = float(osc_tds1002b.send("get_waveform_conversion_factor"))
  yoff = float(osc_tds1002b.send("get_waveform_vertical_offset"))
  xincr = float(osc_tds1002b.send("get_waveform_horizontal_sampling_interval"))

  data = osc_tds1002b.send("get_waveform_data")

  headerlen = 2 + int(data[1])
  header = data[:headerlen]
  ADC_wave = data[headerlen:-1]
  ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))
  Volts = np.append(Volts, (ADC_wave - yoff) * ymult + yzero)
  Time = np.arange(0, xincr * len(Volts), xincr)

  plt.figure(figsize=(20,10))
  plt.plot(Time, Volts)
  plt.grid()
  plt.xlabel("Time")
  plt.ylabel("Voltage [V]")
  plt.show()

else:
  print("Oscilloscope TDS1002B not found")
```
