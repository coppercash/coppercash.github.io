---
title: 'iOS interview knowledge points'
layout: post
---


[@](http://nshipster.com/at-compiler-directives/)

`@class`
`#import`
`#include`

### @autorelease
+ Objc 2.0 有GC，但只有OS X可用
+ drain在GC环境下会触发回收，release不会。非GC环境下二者相同。所以该用drain。
+ autorelease pool 是嵌套的，逻辑模型是栈。
  + 被autorelease的对象总会放入栈顶得pool里。
  + 销毁非栈顶的pool会销毁所有之上的pool
+ AutoReleasePool is drained after every time a **run loop (event-loop)** end.
+ Every dispatch queue maintain its own AutoReleasePool, but it is no guaranteed when will it be drained.

### @encode
```objc
+ (NSValue *)valueWithCGAffineTransform:(CGAffineTransform)transform {
    return [NSValue valueWithBytes:&transform     
						  objCType:@encode(CGAffineTransform)];
}
 
- (CGAffineTransform)CGAffineTransformValue {
    CGAffineTransform transform;
    [self getValue:&transform];
    return transform;
}
```
```objc
char *myCString = "This is a string.";
NSValue *theValue = [NSValue valueWithBytes:&myCString 
							   withObjCType:@encode(char **)];
```
## KVC
### lookup: 
1. method `key` `getKey` `_key` `_getKey`
2. ivar `key` `_key` 
3. `valueForUndefinedKey:`

### `const` `volatile`
+ `int const * const var`
+ `volatile` 防止过度优化，每次访问必须从内存取值，而不是使用寄存器中的cache


## `NULL` `nil` `Nil` `NSNull`
+ `NULL` == `nil`
+ `Nil` pointer of a Class
+ `NSNull` a singleton

## `@protected` `@private` `@public` `@package`

## Singleton

```objc
+ (instancetype)sharedMyObject {
	static MyObject *_instance = nil;
	static dispatch_once_t onceToken;
	dispatch_once(&onceToken, ^{
		_instance = [[MyObject alloc] init];
	});
	return _instance;
}
```
```objc
+ (instancetype)sharedMyObject {
	static MyObject *_instance = nil;
	@synchronize(self) {
		if (nil == _instance) {
			_instance = [[MyObject alloc] init];
		}
	}
	return _instance;
}
```
```swift
class MyObject {
	class func sharedMyObject() -> MyObject {
		struct Singleton {
			static let instance = MyObject()
		}
		return Singleton.instance
	}
}
```
## `+(void)load;` `+(void)initialize;`

| feature | `+(void)load` | `+(void)initialize` |
| :-- | :-- | :-- |
| 执行时机 | 在程序运行后立即执行 | 在类的方法第一次被调时执行 |
| 未定义 | 不会被调用 | 会被调用，使用分类的定义。若无，使用父类的定义 |
| 分类中的定义 | 全都执行，但后于类中的方法 | 覆盖类中的方法，只执行一个 |
| 执行顺序 | 父类，类，分类 | 父类，类（可能使用分类的定义） |
| 是否需要调用 super | 否。否则重复调用 | 否。否则重复调用 |
| 系统调用次数 | 每类1次（分类与类独立存在） | 每类1次（分类合并到类） |
| 调用时机 | 类组装完成之后 | 类函数被调用之前 |
| 能否使用autorelease | 早期版本不能，现在可以 | 通常可以，除非在 `load` 中使用（早期版本） |
| 线程安全 | ？ | 是 |

## `-ObjC`, `-all_load`, `-force_load`
> IMPORTANT: For 64-bit and iPhone OS applications, there is a linker bug that prevents -ObjC from loading objects files from static libraries that contain only categories and no classes. The workaround is to use the -all_load or -force_load flags. -all_load forces the linker to load all object files from every archive it sees, even those without Objective-C code. -force_load is available in Xcode 3.2 and later. It allows finer grain control of archive loading. Each -force_load option must be followed by a path to an archive, and every object file in that archive will be loaded.

## `description` `debugDescription`
+ `-(NSString *)description;` used on UI.
+ `-(NSString *)debugDescription;` has same value with `description` by default. Used in `NSLog(@"%@")` and `po`.

## `Class` `Method` `SEL` `IMP`
```objc
[self.person setValue:@"Vincent" forKey:@"name"];
```
```c
// A method selector is a C string that has been registered (or "mapped") with the Objective-C runtime
SEL sel = sel_get_uid("setValue:forKey:");	
// isa (is a kind of) points to a `Class` struct. `Class` has a member names `methodLists`, which contains linked lists consist of `Method`. Search the list with SEL value can get a `IMP` value, which is a function pointer points to the concrete implement of a method
IMP method = objc_msg_lookup(self.person->isa, sel);
// Invoke the function pointed by `IMP`
method(self.person, sel, @"Vincent", @"name");
```

## Push Notification Device Token 什么时候会变?
After reset system, or restore system from another device's backup.
Every time the app launches, it should register the currently valid token to server, and unregister it when user logout. The invalid tokens can be found via APNs **feedback** function.

## Block

### Features

| Type\Method | retain | copy | release |
| :--: | :-- | :-- | :-- |
| `__NSStackBlock__` | X | Move block to heap from stack (retainCount = 1) | X |
| `__NSMallocBlock__` | retainCount += 1 | retainCount += 1 | retainCount -= 1 |
| `__NSGlobalBlock__` | X | X | X |

| \ | non-ARC | ARC |
| :-- | :-- | :-- |
| `__NSStackBlock__` | construct in function | `__weak` or `__unsafe_unretained` only |
| `__NSMallocBlock__` | `[[a_block copy] autorelease]` | `__strong` or `return` |
| `__NSGlobalBlock__` | construct without capturing vars | construct without capturing vars |

| Block copied to heap | Native | Objc Object |
| :-- | :-- | :-- |
| global/static | keep reference | no-retain |
| local | value copy | retain |
| instance | retain `self` | retain `self` |
| `__block` | `__Block_byref_NAME_INDEX` | `__Block_byref_NAME_INDEX`, no-retain |

### Implement

+ `__{$Scope}_block_impl_{$index} `
  + `__block_impl`
      + `void *isa;`
      + `void *FuncPtr;  // __{$Scope}_block_func_{$index}`
  + `__{$Scope}_block_desc_{$index}`
      + `void (*copy)()  // __{$Scope}_block_copy_{$index}()`
      + `void (*dispose)()  // __{$Scope}_block_dispose_{$index}()`
  + `__Block_byref_{$var_name}_{$index} *{$block_vars}` ...
       + `void *__isa;`  
       + `__Block_byref_{$var_name}_{$index} *__forwarding;`
       + `int {$var_name};`
  + `type {$local_vars}` ...
  + `type *{$static_or_global_vars}` ...

#### Definition

+ `__block_impl`
  + `void *isa`
  + `Flags`
  + `int Flags`
  + `void *FuncPtr  // __{$Scope}_block_func_{$index}`

``` cpp
struct __block_impl {  
    void *isa;  
    int Flags;  
    int Reserved;  
    void *FuncPtr;  
};
```

#### Concrete implement

+ `__{$Scope}_block_impl_{$index}`
  + `struct __block_impl impl`
  + `struct __{$Scope}_block_desc_{$index}* Desc`
  + `type {$local_vars}` ...
  + `type *{$static_or_global_vars}` ...
  + `__Block_byref_{$var_name}_{$index} *{$block_vars}` ...
``` cpp
struct __main_block_impl_0 {  
    struct __block_impl impl;  
    struct __main_block_desc_0* Desc;  
    int i;  
    __main_block_impl_0(void *fp, struct __main_block_desc_0 *desc, int _i, int flags=0) : i(_i) {  
        impl.isa = &_NSConcreteStackBlock;  
        impl.Flags = flags;  
        impl.FuncPtr = fp;  
        Desc = desc;
    }  
};
```

#### Description

+ `__{$Scope}_block_desc_{$index}`
  + `unsigned long reserved`
  + `unsigned long Block_size`
  + `void (*copy)()  // __{$Scope}_block_copy_{$index}()`
  + `void (*dispose)()  // __{$Scope}_block_dispose_{$index}()`
``` cpp
static void __main_block_copy_0(struct __main_block_impl_0*dst, struct __main_block_impl_0*src) {_Block_object_assign((void*)&dst->i, (void*)src->i, 8/*BLOCK_FIELD_IS_BYREF*/);}  
   
static void __main_block_dispose_0(struct __main_block_impl_0*src) {_Block_object_dispose((void*)src->i, 8/*BLOCK_FIELD_IS_BYREF*/);}  
   
static struct __main_block_desc_0 {  
    unsigned long reserved;  
    unsigned long Block_size;  
    void(*copy)(struct __main_block_impl_0*, struct __main_block_impl_0*);  
    void(*dispose)(struct __main_block_impl_0*);  
} __main_block_desc_0_DATA = { 0, sizeof(struct__main_block_impl_0), __main_block_copy_0, __main_block_dispose_0};  
```

#### Block reference

+ `__Block_byref_{$var_name}_{$index}`
  + `void *__isa`
  + `__Block_byref_{$var_name}_{$index} *__forwarding`
  + `int __flags`
  + `int __size`
   + `int {$var_name}`
```cpp
struct __Block_byref_i_0 {  
    void *__isa;  
    __Block_byref_i_0 *__forwarding;  
    int __flags;  
    int __size;  
    int i;  
};  
```

## UIWindow

+ `[UIApplication sharedApplication].windows`
+ `UIWindowLevel`
 `UIWindowLevelAlert` > `UIWindowLevelStatusBar` > `UIWindowLevelNormal`
+ `makeKeyAndVisible`  `resignKeyWindow`
+ `UIView` -> `UIViewController` -> `UIWindow` -> `UIApplication` -> 'AppDelegate'

## Objc Runtime

``` c
typedef struct objc_method *Method;
struct objc_method {
    SEL method_name                                          OBJC2_UNAVAILABLE;
    char *method_types                                       OBJC2_UNAVAILABLE;
    IMP method_imp                                           OBJC2_UNAVAILABLE;
}                                                            OBJC2_UNAVAILABLE;
```

``` objc
#import <objc/runtime.h>
+ (void)swizzleInstanceMethod:(SEL)originalName extendedMethod:(SEL)extendedName {
    // Get methods first
    //
    Method
    originalMethod = class_getInstanceMethod(self, originalName),
    extendedMethod = class_getInstanceMethod(self, extendedName);
    NSAssert(nil != originalMethod, @"Missing original method named '%@'.", NSStringFromSelector(originalName));
    NSAssert(nil != originalMethod, @"Missing extended method named '%@'.", NSStringFromSelector(extendedName));
    
    // Considering the original method is on super class, try add it first
    //
    if (class_addMethod(self, originalName, method_getImplementation(extendedMethod), method_getTypeEncoding(extendedMethod))) {
        class_replaceMethod(self, extendedName, method_getImplementation(originalMethod), method_getTypeEncoding(originalMethod));
    }
    else {
        method_exchangeImplementations(originalMethod, extendedMethod);
    }
}
```

## ARC

### Retainable types

+ `id`
+ `Class`
+ `NSObject`
+ `__attribute__((NSObject)) // e.g. dispatch_queue_t after iOS6`

### Relative C APIs

#### Autorelease
+ `objc_autorelease`
+ `objc_autoreleasePoolPop`
+ `objc_retainAutoreleasedReturnValue`
+ `objc_autoreleaseReturnValue`

#### Weak
+ `objc_loadWeakRetained`

##### Weak refs
`objc_initWeak`
`objc_destroyWeak`
`objc_storeWeak`

##### When object released
`objc_release`
`_objc_rootDealloc`
`object_dispose`
`objc_destructInstance`
`objc_clear_deallocating`

#### Retain count
`_objc_rootRetainCount`

### Forbid ARC

#### Source files
+ `-fobjc-arc`
+ `-fno-objc-arc`

#### Compile time
``` objc
__attribute__((objc_arc_weak_reference_unavailable))
@interface Point : NSObject 
@end
```
#### Runtime
``` objc
- (BOOL)allowsWeakReference; // NS_DEPRECATED
- (BOOL)retainWeakReference; // NS_DEPRECATED
```


