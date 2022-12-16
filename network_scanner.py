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

def get_signal_strength(address):
    return int(parse_interface()[address]['Signal level'].split(' ')[0])

if __name__ == '__main__':
    #interface = 'wlp1s0' # 'wlan0' for rpi
    address = next(iter(parse_interface()))
    print(address, get_signal_strength(address))