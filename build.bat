@echo off
cls
if exist build rmdir /s /q build
mkdir build
nasm src/boot.asm -f bin -o build\boot.bin&&nasm src/kernel_entry.asm -f elf -o build\kernel_entry.o&&gcc -m32 -ffreestanding -c src/kernel.c -o build\kernel.o&&ld -melf_i386 -o build\kernel.bin -Ttext 0x1000 build\kernel_entry.o build\kernel.o --oformat binary&&cat build\boot.bin build\kernel.bin>build\os.bin&&qemu-system-i386 -boot order=a -drive file=build\os.bin,format=raw,index=0,if=floppy
