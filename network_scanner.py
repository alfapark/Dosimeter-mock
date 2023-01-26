import subprocess


def parse_one_cell(cell):
    lines = [line.strip() for line in cell.split('\n')]
    res = dict()
    for line in lines:
        #print(line)
        if '=' in line and '  ' in line:
            for part in line.split('  '):
                key, val = part.split('=', 1)
                res[key] = val.strip()
        elif ':' not in line:
            continue
        else:
            key, val = line.split(':', 1)
            res[key] = val.strip()
    return res

def parse_interface():
    process = subprocess.run(['iwlist', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    s = process.stdout.decode('utf-8')

    l = s.split('Cell ')[1:] # splitting by cell and then removing the initial info

    l = [s[s.index('A'):] for s in l] # remove cell id and dash
    l = [parse_one_cell(c) for c in l] # parse it
    l = {c['Address']:c for c in l} # to dict
    return l

def parse_signal_strength(entry):
    return int(entry['Signal level'].split(' ')[0])

def parse_signal_strengths(parsed_interface = None):
    if parsed_interface is None:
        parsed_interface = parse_interface()
    return { c:parse_signal_strength(parsed_interface[c]) for c in parsed_interface}

def get_signal_strength(address, parsed_interface = None):
    if parsed_interface is None:
        parsed_interface = parse_interface()
    return parse_signal_strength(parsed_interface[address])

if __name__ == '__main__':
    #interface = 'wlp1s0' # 'wlan0' for rpi
    print(parse_signal_strengths())
