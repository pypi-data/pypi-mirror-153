import sys
import os
import tempfile
class basic:
    name = "basic"
    align = 1
    fd = None

    def __init__(self, outfile, align = 1):
        align = int(align)
        self.align = align
        self.outfile = outfile
        self.fd = open(outfile + ".appending", "wb+")

    def append(self, infile):
        infile.seek(0, os.SEEK_END)
        size = infile.tell()
        size -= 64 # size of header
        infile.seek(0)
        '''
        if self.fd.tell() and self.align > 1:
            self.fd.write(b'\00' * self.align)

        infile.seek(0, os.SEEK_END)
        size = infile.tell()
        infile.seek(0)
        '''
        data = infile.read()
        self.fd.write(data)
        infile.close()

        opos = self.fd.tell()
        while opos % self.align > 0:
            self.fd.write(b'\00')
            opos = opos + 1

        if size % self.align:
            self.fd.write(b'\00' * self.align)

    def close(self):
        self.fd.close()
        #Avoid exception on windows 
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
        os.rename(self.outfile + ".appending", self.outfile)

    def describe(self):
        return self.name + "/" + str(self.align) + " bytes"


class physmap(basic):
    name = "physmap"
    def __init__(self, outfile, align):
        super().__init__(outfile, 8)

class SD(basic):
    name = "SD"
    def __init__(self, outfile, align):
        super().__init__(outfile, 512)

class ini(basic):
    name = "ini"
    first = True
    def __init__(self, outfile, align):
        super().__init__(outfile)
    
    def append(self, infile):
        super().append(infile)

        if not self.first:
            self.fd.write(b'\00')

        self.first = False

