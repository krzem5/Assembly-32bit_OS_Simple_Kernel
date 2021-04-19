import subprocess
import sys
import os



if (os.path.exists("build")):
	dl=[]
	for r,ndl,fl in os.walk("build"):
		r=r.replace("\\","/").strip("/")+"/"
		for d in ndl:
			dl.insert(0,r+d)
		for f in fl:
			os.remove(r+f)
	for k in dl:
		os.rmdir(k)
else:
	os.mkdir("build")
if (subprocess.run(["nasm","src/boot.asm","-f","bin","-o","build/boot.bin","-Wall"]).returncode!=0 or subprocess.run(["nasm","src/kernel_entry.asm","-f","elf","-o","build/kernel_entry.o","-Wall"]).returncode!=0 or subprocess.run(["gcc","-m32","-ffreestanding","-c","src/kernel.c","-o","build/kernel.o","-Wall"]).returncode!=0 or subprocess.run(["ld","-melf_i386","-Ttext","0x1000","-o","build/kernel.bin","--oformat","binary","build/kernel_entry.o","build/kernel.o"]).returncode!=0):
	sys.exit(1)
with open("build/os.bin","wb") as wf,open("build/boot.bin","rb") as rf0,open("build/kernel.bin","rb") as rf1:
	wf.write(rf0.read())
	wf.write(rf1.read())
if ("--run" in sys.argv):
	subprocess.run(["qemu-system-i386","-boot","order=a","-drive","file=build/os.bin,format=raw,index=0,if=floppy"])
