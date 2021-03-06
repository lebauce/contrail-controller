#!/usr/bin/python

#
# Copyright (c) 2013 Juniper Networks, Inc. All rights reserved.
#

def generate_header(file):
    header = """//
// Generated by base/factory_macros.py
//

"""
    file.write(header)

macro_tmpl = """#define FACTORY_TYPE_N%(cardinality)d(_Module, _T%(comma)s%(argument_types)s)
  public:
    template <class U>
    static typename boost::enable_if<boost::is_same<U, _T>, void>::type
        Register(boost::function<_T *(%(argument_types)s)> function) {
        _Module *obj = GetInstance();
        obj->make_ ## _T ## _ = function;
    }
    template <class U>
    static typename boost::enable_if<boost::is_same<U, _T>, _T *>::type
        Create(%(argument_decl)s) {
        _Module *obj = GetInstance();
        return obj->make_ ## _T ## _(%(call_arguments)s);
    }
  private:
    boost::function<_T *(%(argument_types)s)> make_ ## _T ##_
"""

def generate_n(file, cardinality):
    call_arguments = ''
    decl = ''
    types = ''

    for n in range(cardinality):
        if n:
            call_arguments += ', '
            decl += ', '
            types += ', '
        call_arguments += 'a%d' % n
        decl += 'A%d a%d' % (n, n)
        types += 'A%d' % n

    if cardinality:
        comma = ', '
    else:
        comma = ''

    macro = macro_tmpl % {
        'argument_decl': decl,
        'argument_types': types,
        'call_arguments': call_arguments,
        'cardinality': cardinality,
        'comma': comma,
        }

    file.write(macro.replace('\n', '\\\n'))
    file.write('\n')

def generate(filename):
    file = open(filename, 'w')
    generate_header(file)
    for n in range(8):
        generate_n(file, n)
    file.close()

if __name__ == '__main__':
    generate("src/base/factory_macros.h")
