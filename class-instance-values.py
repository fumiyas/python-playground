#!/usr/bin/env python3
# -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

class Foo:
    s1 = "Foo 1"
    s2 = "Foo 2"
    i1 = 100
    i2 = 200

    def __init__(self, suffix: str, additional: int):
        self.s1 += f" {suffix}"
        self.i1 += additional
        Foo.s2 += f" {suffix}"
        Foo.i2 += additional

    def strings(self):
        print(id(self.s1), "/", id(self.s2), self.s1, "/", self.s2)

    def integers(self):
        print(id(self.i1), "/", id(self.i2), self.i1, "/", self.i2)


Foo.i1 += 1

foo1 = Foo("foo1", 11)
foo2 = Foo("foo2", 22)

foo1.strings()
foo2.strings()
print(id(Foo.s1), "/", id(Foo.s2), Foo.s1, "/", Foo.s2)

print()
foo1.integers()
foo2.integers()
print(id(Foo.i1), "/", id(Foo.i2), Foo.i1, "/", Foo.i2)
