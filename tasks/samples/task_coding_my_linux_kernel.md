---

## 任务

- **任务编号**：T-01-01

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：kernel_types.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位微内核基础类型头文件，固定typedef：u8、u16、u32、u64、s8、s16、s32、s64。

4. 定义宏NULL、运行状态枚举RET_SUCCESS/RET_FAIL。

5. 添加#ifndef防重复包含，作为全内核唯一基础类型定义文件。

- **依赖文件**：

- **任务类型**：PROGRAMMING

---

## 任务

- **任务编号**：T-01-02

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：kernel_global.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 基于kernel_types.h生成全局硬件、内存常量头文件。

4. 定义内存宏、VGA显存、串口、PIT、键盘端口宏。

5. 定义通用双向链表结构体、全局错误码宏。

6. 添加#ifndef防重复包含，禁止各模块自行硬编码硬件地址。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-03

- **文件存储路径**：simple-linux-kernel/boot

- **文件名**：boot.asm

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 采用NASM64汇编编写，实现16位实模式初始化、关中断、开启A20。

4. 加载GDT切换长模式，栈大小严格引用全局宏定义。

5. 最终跳转C语言入口kernel_main。

6. 仅输出可直接编译的汇编代码，所有功能说明全部写在汇编注释内。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-04

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：gdt.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位GDT标准头文件，定义GDT描述符结构体、段选择子枚举。

4. 固定函数原型：void gdt_init(void);、void gdt_load(void);。

5. 添加#ifndef防重复包含，结构体与函数原型固定不可修改。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-05

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：gdt.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 严格依照gdt.h头文件实现64位GDT功能逻辑。

4. 实现gdt_init、gdt_load函数，初始化空段、代码段、数据段。

5. 所有硬件地址、内存常量均引用全局头文件，不新增接口、不修改结构体。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/gdt.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-06

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：idt.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位IDT中断头文件，定义中断门描述符结构体、异常/中断向量枚举。

4. 固定接口：void idt_init(void);、void enable_interrupt(void);、void disable_interrupt(void);。

5. 定义统一中断回调函数指针类型，添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-07

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：idt.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 基于idt.h实现64位IDT基础中断逻辑。

4. 实现idt_init函数初始化中断表，实现开关中断函数。

5. 编写默认异常处理空实现，严禁修改头文件函数原型。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/idt.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-08

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：mm.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位内存管理头文件，定义页目录、页表结构体。

4. 固定接口：void mm_init(void);、u64 pmm_alloc_page(void);、void pmm_free_page(u64 addr);、void* kmalloc(u64 size);、void kfree(void* ptr);。

5. 定义分页基础宏，添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-09

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：mm.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 基于mm.h实现64位内存管理逻辑。

4. mm_init按全局内存范围初始化，实现物理页分配、释放，kmalloc/kfree功能。

5. 不自定义任何内存地址、硬件常量，全部引用全局头文件。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/mm.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-10

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：console.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位控制台统一接口头文件。

4. 固定接口：void console_init(void);、void printf(const char* fmt, ...);、void puts(const char* str);、u8 getchar(void);。

5. 添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-11

- **文件存储路径**：simple-linux-kernel/driver

- **文件名**：console.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位串口+VGA控制台底层代码。

4. console_init完成硬件初始化，实现printf、puts、getchar功能。

5. 所有硬件端口、显存地址均引用全局头文件。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/console.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-12

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：process.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位进程PCB头文件，PCB结构体字段顺序固定不可改动。

4. 定义进程状态枚举，固定接口：void process_init(void);、int create_process(void (*entry)(void));。

5. 添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/mm.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-13

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：process.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位进程管理代码，process_init初始化进程链表。

4. create_process完成进程创建、PCB分配。

5. 严禁修改PCB结构体字段，严格遵循头文件接口。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/mm.h

simple-linux-kernel/include/process.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-14

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：scheduler.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位调度器头文件，定义就绪队列结构。

4. 固定接口：void scheduler_init(void);、void schedule(void);、void switch_process(void);。

5. 定义时间片宏，添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/process.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-15

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：scheduler.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位时间片轮转调度功能。

4. scheduler_init初始化队列，schedule完成进程挑选。

5. 调用switch_process实现进程上下文切换，不修改头文件接口。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/process.h

simple-linux-kernel/include/scheduler.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-16

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：switch.asm

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 采用NASM64汇编生成64位进程上下文切换代码。

4. 严格匹配process.h的PCB结构体偏移，完成寄存器保存与恢复。

5. 实现switch_process函数，所有说明全部写在汇编注释内，仅输出纯净汇编代码。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/process.h

simple-linux-kernel/include/scheduler.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-17

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：syscall.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位系统调用头文件，定义系统调用号枚举。

4. 固定接口：void syscall_init(void);、void syscall_handler(void);。

5. 添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/idt.h

simple-linux-kernel/include/process.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-18

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：syscall.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位系统调用分发逻辑，syscall_init注册中断门。

4. syscall_handler按系统调用号完成功能分发。

5. 严禁改动头文件接口，严格遵循函数原型。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/idt.h

simple-linux-kernel/include/process.h

simple-linux-kernel/include/syscall.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-19

- **文件存储路径**：simple-linux-kernel/driver

- **文件名**：keyboard.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位PS2键盘驱动，keyboard_init初始化键盘中断。

4. 完成扫描码转字符功能，对接console输入接口。

5. 硬件端口常量全部引用全局头文件，禁止硬编码。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/idt.h

simple-linux-kernel/include/console.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-20

- **文件存储路径**：simple-linux-kernel/driver

- **文件名**：vga.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位VGA文本驱动，vga_init完成清屏、光标初始化。

4. 实现字符绘制、屏幕滚动、光标移动功能。

5. 显存地址仅使用全局头文件定义的VGA_BUFFER_ADDR，不自定义地址。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/console.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-21

- **文件存储路径**：simple-linux-kernel/driver

- **文件名**：timer.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位PIT定时器驱动，timer_init初始化时钟中断。

4. 时钟中断内调用schedule函数触发进程调度。

5. 硬件端口引用全局头文件，禁止硬编码。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/idt.h

simple-linux-kernel/include/scheduler.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-22

- **文件存储路径**：simple-linux-kernel/include

- **文件名**：fs.h

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 生成64位文件系统头文件，定义文件、目录项结构体。

4. 固定接口：void fs_init(void);、int file_open(const char* path);、int file_read(int fd, void* buf, u64 len);、int file_write(int fd, const void* buf, u64 len);、void file_close(int fd);。

5. 添加#ifndef防重复包含。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/mm.h

simple-linux-kernel/include/syscall.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-23

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：fs.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 实现64位轻量文件系统，fs_init完成文件系统初始化。

4. 实现file_open、file_read、file_write、file_close基础功能。

5. 严格遵循fs.h头文件接口，不修改结构体与函数原型。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/mm.h

simple-linux-kernel/include/syscall.h

simple-linux-kernel/include/fs.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-24

- **文件存储路径**：simple-linux-kernel

- **文件名**：linker.ld

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 编写64位内核链接脚本，内存地址完全使用kernel_global.h内宏定义。

4. 划分.text、.data、.bss、.stack程序段，栈大小匹配KERNEL_STACK_SIZE。

5. 仅输出纯净链接脚本代码，说明文字写入脚本注释。

- **依赖文件**：

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-25

- **文件存储路径**：simple-linux-kernel

- **文件名**：Makefile

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 编写64位工程编译Makefile，编译boot、kernel、driver目录下所有源码文件。

4. 适配nasm、gcc、ld工具链，搭配linker.ld完成链接。

5. 实现all、clean编译指令，生成kernel.bin内核镜像，仅输出纯净Makefile代码。

- **依赖文件**：

simple-linux-kernel/linker.ld

simple-linux-kernel/include/kernel_global.h

- **任务类型**：PROGRAMMING
---

## 任务

- **任务编号**：T-01-26

- **文件存储路径**：simple-linux-kernel/kernel

- **文件名**：main.c

- **任务要求**：

1. 必须严格遵守全局通用契约：.h头文件作为只读契约，.c/.asm实现文件只适配、不许修改头文件结构与函数原型；所有初始化函数统一命名为`xxx_init(void)`；基础类型、硬件地址、内存常量，只允许引用`kernel_types.h`/`kernel_global.h`，禁止硬编码；C语言统一使用GNU C标准，汇编统一使用NASM64。

2. 必须严格遵守最高强制输出规则：生成内容只能是纯代码 + 代码内部注释；禁止任何文件说明、功能介绍、多余话术、解释文字、非代码描述；不允许出现「以下是代码」「本文件作用」这类非注释文字；如有功能说明、文件用途，只能写在// 或/* */代码注释内；代码块外不允许有任何多余中文、英文文字。

3. 编写64位内核入口代码，入口函数名固定为kernel_main。

4. 按规范顺序调用所有模块xxx_init()初始化函数。

5. 创建空闲进程、开启全局中断，进入内核调度循环。

6. 所有功能说明、注释写入代码内部，不出现代码外多余文字。

- **依赖文件**：

simple-linux-kernel/include/kernel_types.h

simple-linux-kernel/include/kernel_global.h

simple-linux-kernel/include/gdt.h

simple-linux-kernel/include/idt.h

simple-linux-kernel/include/mm.h

simple-linux-kernel/include/console.h

simple-linux-kernel/include/process.h

simple-linux-kernel/include/scheduler.h

simple-linux-kernel/include/syscall.h

simple-linux-kernel/include/fs.h

- **任务类型**：PROGRAMMING
---
