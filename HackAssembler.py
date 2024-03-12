import sys

class Parser:
  def __init__(self,inst):
    self.inst = inst.strip()
    self.tipo = None
    self.valorinst = None
    self.destV = None
    self.compV = None
    self.jumpV = None
    self.limpiar()
    self.tipoInstruccion()

  def tipoInstruccion(self):
    if self.inst == '':
      return
    elif self.inst.startswith('@'):
      self.tipo='A'
      self.valorinst = self.inst[1:]
    elif self.inst.startswith('('):
      self.tipo='L'
    else:
      self.tipo='C'
      
  def valor(self):
    if self.tipo != 'A':
      return None
    return Code.valorA(self.valorinst)


  def limpiar(self):
    self.inst = (self.inst.strip())
    cInd = self.inst.find('//')
    if cInd == -1:
      self.inst = self.inst.strip()
    elif cInd == 0:
      self.inst = ''
    else:
      self.inst = self.inst[0:cInd]
    self.inst = self.inst.strip()

  def dest(self):
    eInd = self.inst.find('=')
    if self.tipo != 'C' or eInd == -1:
       return None     
    self.destV = self.inst[0:eInd].strip()
    return self.destV
  
  def comp(self):
    eInd = self.inst.find('=')
    sInd = self.inst.find(';')
    if self.tipo != 'C':
      return None
    if eInd != -1 and sInd != -1:
      self.compV = self.inst[eInd+1:sInd].strip()
    elif eInd != -1 and sInd == -1:
      self.compV = self.inst[eInd+1:].strip()
    elif eInd == -1 and sInd != -1:
      self.compV = self.inst[0:sInd].strip()
    elif eInd == -1 and sInd == 1:
      self.compV = self.inst.strip()
    return self.compV

  def jump(self):
    eInd = self.inst.find(';')
    if self.tipo != 'C' or eInd == -1:
      return None
    self.jumpV = self.inst[eInd+1:].strip()
    return self.jumpV
  
class Code:
        
    @staticmethod
    def comp(mnemonico):
        codigosComp = {'0': '101010',
                   '1':'111111',
                   '-1':'111010',
                   'D':'001100',
                   'A':'110000',
                   '!D':'001101',
                   '!A':'110001',
                   '-D':'001111',
                   '-A':'110011',
                   'D+1':'011111',
                   'A+1':'110111',
                   'D-1':'001110',
                   'A-1':'110010',
                   'D+A':'000010',
                   'D-A':'010011',
                   'A-D':'000111',
                   'D&A':'000000',
                   'D|A':'010101',
                   'M':'110000',
                   '!M':'110001',
                   '-M':'110011',
                   'M+1':'110111',
                   'M-1':'110010',
                   'D+M':'000010',
                   'D-M':'010011',
                   'M-D':'000111',
                   'D&M':'000000',
                   'D|M':'010101'}
        return codigosComp.get(mnemonico, '000000')
    
    
    @staticmethod
    def dest(mnemonico):
       codigosDest =  {'null': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'DM': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111',
            'ADM': '111' }
       return codigosDest.get(mnemonico, '000')
    
    @staticmethod
    def jump(mnemonico):
       codigosJump = {'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111' }
       return codigosJump.get(mnemonico, '000')
    
    @staticmethod
    def valorA(valor):
        valordecimal = int(valor)
        valorbinario = format(valordecimal, '015b')
        return valorbinario
    
     
    
class SymbolTable:
   def __init__(self):
      self.symtable = {'R0': '0',
                       'R1': '1',
                       'R2': '2',
                       'R3': '3',
                       'R4': '4',
                       'R5': '5',
                       'R6': '6',
                       'R7': '7',
                       'R8': '8',
                       'R9': '9',
                       'R10': '10',
                       'R11': '11',
                       'R12': '12',
                       'R13': '13',
                       'R14': '14',
                       'R15': '15',
                       'SCREEN': '16384',
                       'KBD': '24576',
                       'SP': '0',
                       'LCL': '1',
                       'ARG': '2',
                       'THIS': '3',
                       'THAT': '4',
                       'LOOP': '4',
                       'STOP': '18',
                       'i': '16',
                       'sum': '17',
                       'END': '22'}

   def agregar(self, simbolo, direccion):
      self.symtable[simbolo] = direccion

   def contiene(self, simbolo):
      if simbolo in self.symtable:
         return True
      else:
         return False
      
   def buscardireccion(self, simbolo):
      return self.symtable.get(simbolo)


def main():
    salida = "Prog.hack"
    with open(sys.argv[1], 'r') as asm, open(salida, 'w') as archivohack:
        for inst in asm:
            p = Parser(inst)
            code = Code()
            symboltable = SymbolTable()
            nuevainst = ""
            print(p.inst)
            if p.tipo == 'A':
              instlimpia = p.inst.replace("@", "")
              if instlimpia.isdigit():
                 instbin = code.valorA(instlimpia)
                 nuevainst = '0' + instbin
                 print(nuevainst)
                 archivohack.write(nuevainst + '\n')
              else:
                 if symboltable.contiene(instlimpia) == True:
                  dir = symboltable.buscardireccion(instlimpia)
                  dir = code.valorA(dir)        
                  print('0' + dir)  
                  archivohack.write('0' + dir + '\n')
            elif p.tipo == 'C':
                if p.comp() is not None:
                   if 'M' in p.comp():
                     nuevainst = '1111' + code.comp(p.comp()) + code.dest(p.dest()) + code.jump(p.jump())
                   else:
                     nuevainst = '1110' + code.comp(p.comp()) + code.dest(p.dest()) + code.jump(p.jump())
                   print(nuevainst)
                   archivohack.write(nuevainst + '\n')
            elif p.tipo == 'L':
                pass
               
      


if __name__  == "__main__":
   main()

