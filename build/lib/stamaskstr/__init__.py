name="stamaskstr"

import uuid, hashlib, base64, string, random

def uid():
    return "".join([chr(int(i)+64) if int(i) % 2 else chr(int(i)+96) for i in list(str(uuid.getnode()))])

def Hash(clean):
    """
    Uses a clean string and generate a hash.
    """
    return hashlib.sha256(str((clean)).encode()).hexdigest()
    
def HashCheck(clean, hsh):
    """
    get a clean string and the hash (you can generate it using Hash function) and validate it
    """
    return Hash(clean) == hsh

def mask(mk):
    """
    mask the string
    """
    msk=[]
    for i in range(len(mk)):
        ch = list(''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(len(mk))))
        ch[(i-1)+1:(i-1)+2] = mk[i]
        msk.append("".join(ch[::-1]))
    
    msk.append(chr(len(mk)+96))
    msk.append(uid())
    return base64.urlsafe_b64encode("".join(msk).encode()).decode()

def masked(mk, hsh):
    """
    Get the masked string and hash and unmask it
    """
    base=base64.urlsafe_b64decode(mk.encode()).decode()
    if base[-len(uid()):] == uid():
        N = (ord(base[:-len(uid())][-1:])-96)
        msk=[base[i:i+N] for i in range(0, len(base[:-len(uid())]), N)]
        umsk=[]
        for i in range(len(msk)-1):
            umsk.append(msk[i][::-1][i])
    if Hash("".join(umsk)) == hsh:
        return "".join(umsk)
    return False

def simplem(smk):
    """
    simple mask based on b64
    """
    return base64.urlsafe_b64encode(smk[::-1].encode()).decode()

def simplemkd(smk):
    """
    unmask string masked by simplem
    """
    return base64.urlsafe_b64decode(smk.encode()).decode()[::-1]