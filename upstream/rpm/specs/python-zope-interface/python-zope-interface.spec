%define name zope.interface
%define version 3.6.1
%define unmangled_version 3.6.1
%define unmangled_version 3.6.1
%define release 1
%define _relstr 0contrail

Summary: Interfaces for Python
Name: python-zope-interface 
Version: %{version}
Release: %{release}.%{_relstr}
Source0: https://pypi.python.org/packages/source/z/zope.interface/zope.interface-3.6.1.tar.gz 
License: ZPL 2.1
Group: Development/Libraries

Prefix: %{_prefix}
Vendor: Zope Foundation and Contributors <zope-dev@zope.org>
Url: http://pypi.python.org/pypi/zope.interface

%description
*This package is intended to be independently reusable in any Python
project. It is maintained by the* `Zope Toolkit project <http://docs.zope.org/zopetoolkit/>`_.

This package provides an implementation of `object interfaces` for Python.
Interfaces are a mechanism for labeling objects as conforming to a given
API or contract. So, this package can be considered as implementation of
the `Design By Contract`_ methodology support in Python.

.. _Design By Contract: http://en.wikipedia.org/wiki/Design_by_contract

Detailed Documentation
**********************

.. contents::

==========
Interfaces
==========

Interfaces are objects that specify (document) the external behavior
of objects that "provide" them.  An interface specifies behavior
through:

- Informal documentation in a doc string

- Attribute definitions

- Invariants, which are conditions that must hold for objects that
  provide the interface

Attribute definitions specify specific attributes. They define the
attribute name and provide documentation and constraints of attribute
values.  Attribute definitions can take a number of forms, as we'll
see below.

Defining interfaces
===================

Interfaces are defined using Python class statements::

  >>> import zope.interface
  >>> class IFoo(zope.interface.Interface):
  ...    """Foo blah blah"""
  ...
  ...    x = zope.interface.Attribute("""X blah blah""")
  ...
  ...    def bar(q, r=None):
  ...        """bar blah blah"""

In the example above, we've created an interface, `IFoo`.  We
subclassed `zope.interface.Interface`, which is an ancestor interface for
all interfaces, much as `object` is an ancestor of all new-style
classes [#create]_.   The interface is not a class, it's an Interface,
an instance of `InterfaceClass`::

  >>> type(IFoo)
  <class 'zope.interface.interface.InterfaceClass'>

We can ask for the interface's documentation::

  >>> IFoo.__doc__
  'Foo blah blah'

and its name::

  >>> IFoo.__name__
  'IFoo'

and even its module::

  >>> IFoo.__module__
  '__main__'

The interface defined two attributes:

`x`
  This is the simplest form of attribute definition.  It has a name
  and a doc string.  It doesn't formally specify anything else.

`bar`
  This is a method.  A method is defined via a function definition.  A
  method is simply an attribute constrained to be a callable with a
  particular signature, as provided by the function definition.

  Note that `bar` doesn't take a `self` argument.  Interfaces document
  how an object is *used*.  When calling instance methods, you don't
  pass a `self` argument, so a `self` argument isn't included in the
  interface signature.  The `self` argument in instance methods is
  really an implementation detail of Python instances. Other objects,
  besides instances can provide interfaces and their methods might not
  be instance methods. For example, modules can provide interfaces and
  their methods are usually just functions.  Even instances can have
  methods that are not instance methods.

You can access the attributes defined by an interface using mapping
syntax::

  >>> x = IFoo['x']
  >>> type(x)
  <class 'zope.interface.interface.Attribute'>
  >>> x.__name__
  'x'
  >>> x.__doc__
  'X blah blah'

  >>> IFoo.get('x').__name__
  'x'

  >>> IFoo.get('y')

You can use `in` to determine if an interface defines a name::

  >>> 'x' in IFoo
  True

You can iterate over interfaces to get the names they define::

  >>> names = list(IFoo)
  >>> names.sort()
  >>> names
  ['bar', 'x']

Remember that interfaces aren't classes. You can't access attribute
definitions as attributes of interfaces::

  >>> IFoo.x
  Traceback (most recent call last):
    File "<stdin>", line 1, in ?
  AttributeError: 'InterfaceClass' object has no attribute 'x'

Methods provide access to the method signature::

  >>> bar = IFoo['bar']
  >>> bar.getSignatureString()
  '(q, r=None)'

TODO
  Methods really should have a better API.  This is something that
  needs to be improved.

Declaring interfaces
====================

Having defined interfaces, we can *declare* that objects provide
them.  Before we describe the details, lets define some terms:

*provide*
   We say that objects *provide* interfaces.  If an object provides an
   interface, then the interface specifies the behavior of the
   object. In other words, interfaces specify the behavior of the
   objects that provide them.

*implement*
   We normally say that classes *implement* interfaces.  If a class
   implements an interface, then the instances of the class provide
   the interface.  Objects provide interfaces that their classes
   implement [#factory]_.  (Objects can provide interfaces directly,
   in addition to what their classes implement.)

   It is important to note that classes don't usually provide the
   interfaces that they implement.

   We can generalize this to factories.  For any callable object we
   can declare that it produces objects that provide some interfaces
   by saying that the factory implements the interfaces.

Now that we've defined these terms, we can talk about the API for
declaring interfaces.

Declaring implemented interfaces
--------------------------------

The most common way to declare interfaces is using the implements
function in a class statement::

  >>> class Foo:
  ...     zope.interface.implements(IFoo)
  ...
  ...     def __init__(self, x=None):
  ...         self.x = x
  ...
  ...     def bar(self, q, r=None):
  ...         return q, r, self.x
  ...
  ...     def __repr__(self):
  ...         return "Foo(%s)" % self.x


In this example, we declared that `Foo` implements `IFoo`. This means
that instances of `Foo` provide `IFoo`.  Having made this declaration,
there are several ways we can introspect the declarations.  First, we
can ask an interface whether it is implemented by a class::

  >>> IFoo.implementedBy(Foo)
  True

And we can ask whether an interface is provided by an object::

  >>> foo = Foo()
  >>> IFoo.providedBy(foo)
  True

Of course, `Foo` doesn't provide `IFoo`, it implements it::

  >>> IFoo.providedBy(Foo)
  False

We can also ask what interfaces are implemented by an object::

  >>> list(zope.interface.implementedBy(Foo))
  [<InterfaceClass __main__.IFoo>]

It's an error to ask for interfaces implemented by a non-callable
object::

  >>> IFoo.implementedBy(foo)
  Traceback (most recent call last):
  ...
  TypeError: ('ImplementedBy called for non-factory', Foo(None))

  >>> list(zope.interface.implementedBy(foo))
  Traceback (most recent call last):
  ...
  TypeError: ('ImplementedBy called for non-factory', Foo(None))

Similarly, we can ask what interfaces are provided by an object::

  >>> list(zope.interface.providedBy(foo))
  [<InterfaceClass __main__.IFoo>]
  >>> list(zope.interface.providedBy(Foo))
  []

We can declare interfaces implemented by other factories (besides
classes).  We do this using a Python-2.4-style decorator named
`implementer`.  In versions of Python before 2.4, this looks like::

  >>> def yfoo(y):
  ...     foo = Foo()
  ...     foo.y = y
  ...     return foo
  >>> yfoo = zope.interface.implementer(IFoo)(yfoo)

  >>> list(zope.interface.implementedBy(yfoo))
  [<InterfaceClass __main__.IFoo>]

Note that the implementer decorator may modify it's argument. Callers
should not assume that a new object is created.

Using implementer also works on callable objects. This is used by
zope.formlib, as an example.

  >>> class yfactory:
  ...     def __call__(self, y):
  ...         foo = Foo()
  ...         foo.y = y
  ...         return foo
  >>> yfoo = yfactory()
  >>> yfoo = zope.interface.implementer(IFoo)(yfoo)

  >>> list(zope.interface.implementedBy(yfoo))
  [<InterfaceClass __main__.IFoo>]

XXX: Double check and update these version numbers:

In zope.interface 3.5.2 and lower, the implementor decorator can not
be used for classes, but in 3.6.0 and higher it can:

  >>> Foo = zope.interface.implementer(IFoo)(Foo)
  >>> list(zope.interface.providedBy(Foo()))
  [<InterfaceClass __main__.IFoo>]
  
Note that class decorators using the @implementor(IFoo) syntax are only 
supported in Python 2.6 and later.


Declaring provided interfaces
-----------------------------

We can declare interfaces directly provided by objects.  Suppose that
we want to document what the `__init__` method of the `Foo` class
does.  It's not *really* part of `IFoo`.  You wouldn't normally call
the `__init__` method on Foo instances.  Rather, the `__init__` method
is part of the `Foo`'s `__call__` method::

  >>> class IFooFactory(zope.interface.Interface):
  ...     """Create foos"""
  ...
  ...     def __call__(x=None):
  ...         """Create a foo
  ...
  ...         The argument provides the initial value for x ...
  ...         """

It's the class that provides this interface, so we declare the
interface on the class::

  >>> zope.interface.directlyProvides(Foo, IFooFactory)

And then, we'll see that Foo provides some interfaces::

  >>> list(zope.interface.providedBy(Foo))
  [<InterfaceClass __main__.IFooFactory>]
  >>> IFooFactory.providedBy(Foo)
  True

Declaring class interfaces is common enough that there's a special
declaration function for it, `classProvides`, that allows the
declaration from within a class statement::

  >>> class Foo2:
  ...     zope.interface.implements(IFoo)
  ...     zope.interface.classProvides(IFooFactory)
  ...
  ...     def __init__(self, x=None):
  ...         self.x = x
  ...
  ...     def bar(self, q, r=None):
  ...         return q, r, self.x
  ...
  ...     def __repr__(self):
  ...         return "Foo(%s)" % self.x

  >>> list(zope.interface.providedBy(Foo2))
  [<InterfaceClass __main__.IFooFactory>]
  >>> IFooFactory.providedBy(Foo2)
  True

There's a similar function, `moduleProvides`, that supports interface
declarations from within module definitions.  For example, see the use
of `moduleProvides` call in `zope.interface.__init__`, which declares that
the package `zope.interface` provides `IInterfaceDeclaration`.

Sometimes, we want to declare interfaces on instances, even though
those instances get interfaces from their classes.  Suppose we create
a new interface, `ISpecial`::

  >>> class ISpecial(zope.interface.Interface):
  ...     reason = zope.interface.Attribute("Reason why we're special")
  ...     def brag():
  ...         "Brag about being special"

We can make an existing foo instance special by providing `reason`
and `brag` attributes::

  >>> foo.reason = 'I just am'
  >>> def brag():
  ...      return "I'm special!"
  >>> foo.brag = brag
  >>> foo.reason
  'I just am'
  >>> foo.brag()
  "I'm special!"

and by declaring the interface::

  >>> zope.interface.directlyProvides(foo, ISpecial)

then the new interface is included in the provided interfaces::

  >>> ISpecial.providedBy(foo)
  True
  >>> list(zope.interface.providedBy(foo))
  [<InterfaceClass __main__.ISpecial>, <InterfaceClass __main__.IFoo>]

We can find out what interfaces are directly provided by an object::

  >>> list(zope.interface.directlyProvidedBy(foo))
  [<InterfaceClass __main__.ISpecial>]

  >>> newfoo = Foo()
  >>> list(zope.interface.directlyProvidedBy(newfoo))
  []

Inherited declarations
----------------------

Normally, declarations are inherited::

  >>> class SpecialFoo(Foo):
  ...     zope.interface.implements(ISpecial)
  ...     reason = 'I just am'
  ...     def brag(self):
  ...         return "I'm special because %s" % self.reason

  >>> list(zope.interface.implementedBy(SpecialFoo))
  [<InterfaceClass __main__.ISpecial>, <InterfaceClass __main__.IFoo>]

  >>> list(zope.interface.providedBy(SpecialFoo()))
  [<InterfaceClass __main__.ISpecial>, <InterfaceClass __main__.IFoo>]

Sometimes, you don't want to inherit declarations.  In that case, you
can use `implementsOnly`, instead of `implements`::

  >>> class Special(Foo):
  ...     zope.interface.implementsOnly(ISpecial)
  ...     reason = 'I just am'
  ...     def brag(self):
  ...         return "I'm special because %s" % self.reason

  >>> list(zope.interface.implementedBy(Special))
  [<InterfaceClass __main__.ISpecial>]

  >>> list(zope.interface.providedBy(Special()))
  [<InterfaceClass __main__.ISpecial>]

External declarations
---------------------

Normally, we make implementation declarations as part of a class
definition. Sometimes, we may want to make declarations from outside
the class definition. For example, we might want to declare interfaces
for classes that we didn't write.  The function `classImplements` can
be used for this purpose::

  >>> class C:
  ...     pass

  >>> zope.interface.classImplements(C, IFoo)
  >>> list(zope.interface.implementedBy(C))
  [<InterfaceClass __main__.IFoo>]

We can use `classImplementsOnly` to exclude inherited interfaces::

  >>> class C(Foo):
  ...     pass

  >>> zope.interface.classImplementsOnly(C, ISpecial)
  >>> list(zope.interface.implementedBy(C))
  [<InterfaceClass __main__.ISpecial>]



Declaration Objects
-------------------

When we declare interfaces, we create *declaration* objects.  When we
query declarations, declaration objects are returned::

  >>> type(zope.interface.implementedBy(Special))
  <class 'zope.interface.declarations.Implements'>

Declaration objects and interface objects are similar in many ways. In
fact, they share a common base class.  The important thing to realize
about them is that they can be used where interfaces are expected in
declarations. Here's a silly example::

  >>> class Special2(Foo):
  ...     zope.interface.implementsOnly(
  ...          zope.interface.implementedBy(Foo),
  ...          ISpecial,
  ...          )
  ...     reason = 'I just am'
  ...     def brag(self):
  ...         return "I'm special because %s" % self.reason

The declaration here is almost the same as
``zope.interface.implements(ISpecial)``, except that the order of
interfaces in the resulting declaration is different::

  >>> list(zope.interface.implementedBy(Special2))
  [<InterfaceClass __main__.IFoo>, <InterfaceClass __main__.ISpecial>]


Interface Inheritance
=====================

Interfaces can extend other interfaces. They do this simply by listing
the other interfaces as base interfaces::

  >>> class IBlat(zope.interface.Interface):
  ...     """Blat blah blah"""
  ...
  ...     y = zope.interface.Attribute("y blah blah")
  ...     def eek():
  ...         """eek blah blah"""

  >>> IBlat.__bases__
  (<InterfaceClass zope.interface.Interface>,)

  >>> class IBaz(IFoo, IBlat):
  ...     """Baz blah"""
  ...     def eek(a=1):
  ...         """eek in baz blah"""
  ...

  >>> IBaz.__bases__
  (<InterfaceClass __main__.IFoo>, <InterfaceClass __main__.IBlat>)

  >>> names = list(IBaz)
  >>> names.sort()
  >>> names
  ['bar', 'eek', 'x', 'y']

Note that `IBaz` overrides eek::

  >>> IBlat['eek'].__doc__
  'eek blah blah'
  >>> IBaz['eek'].__doc__
  'eek in baz blah'

We were careful to override eek in a compatible way.  When extending
an interface, the extending interface should be compatible [#compat]_
with the extended interfaces.

We can ask whether one interface extends another::

  >>> IBaz.extends(IFoo)
  True
  >>> IBlat.extends(IFoo)
  False

Note that interfaces don't extend themselves::

  >>> IBaz.extends(IBaz)
  False

Sometimes we wish they did, but we can, instead use `isOrExtends`::

  >>> IBaz.isOrExtends(IBaz)
  True
  >>> IBaz.isOrExtends(IFoo)
  True
  >>> IFoo.isOrExtends(IBaz)
  False

When we iterate over an interface, we get all of the names it defines,
including names defined by base interfaces. Sometimes, we want *just*
the names defined by the interface directly. We bane use the `names`
method for that::

  >>> list(IBaz.names())
  ['eek']

Inheritance of attribute specifications
---------------------------------------

An interface may override attribute definitions from base interfaces.
If two base interfaces define the same attribute, the attribute is
inherited from the most specific interface. For example, with::

  >>> class IBase(zope.interface.Interface):
  ...
  ...     def foo():
  ...         "base foo doc"

  >>> class IBase1(IBase):
  ...     pass

  >>> class IBase2(IBase):
  ...
  ...     def foo():
  ...         "base2 foo doc"

  >>> class ISub(IBase1, IBase2):
  ...     pass

ISub's definition of foo is the one from IBase2, since IBase2 is more
specific that IBase::

  >>> ISub['foo'].__doc__
  'base2 foo doc'

Note that this differs from a depth-first search.

Sometimes, it's useful to ask whether an interface defines an
attribute directly.  You can use the direct method to get a directly
defined definitions::

  >>> IBase.direct('foo').__doc__
  'base foo doc'

  >>> ISub.direct('foo')

Specifications
--------------

Interfaces and declarations are both special cases of specifications.
What we described above for interface inheritance applies to both
declarations and specifications.  Declarations actually extend the
interfaces that they declare::

  >>> class Baz(object):
  ...     zope.interface.implements(IBaz)

  >>> baz_implements = zope.interface.implementedBy(Baz)
  >>> baz_implements.__bases__
  (<InterfaceClass __main__.IBaz>, <implementedBy ...object>)

  >>> baz_implements.extends(IFoo)
  True

  >>> baz_implements.isOrExtends(IFoo)
  True
  >>> baz_implements.isOrExtends(baz_implements)
  True

Specifications (interfaces and declarations) provide an `__sro__`
that lists the specification and all of it's ancestors::

  >>> baz_implements.__sro__
  (<implementedBy __main__.Baz>,
   <InterfaceClass __main__.IBaz>,
   <InterfaceClass __main__.IFoo>,
   <InterfaceClass __main__.IBlat>,
   <InterfaceClass zope.interface.Interface>,
   <implementedBy ...object>)


Tagged Values
=============

Interfaces and attribute descriptions support an extension mechanism,
borrowed from UML, called "tagged values" that lets us store extra
data::

  >>> IFoo.setTaggedValue('date-modified', '2004-04-01')
  >>> IFoo.setTaggedValue('author', 'Jim Fulton')
  >>> IFoo.getTaggedValue('date-modified')
  '2004-04-01'
  >>> IFoo.queryTaggedValue('date-modified')
  '2004-04-01'
  >>> IFoo.queryTaggedValue('datemodified')
  >>> tags = list(IFoo.getTaggedValueTags())
  >>> tags.sort()
  >>> tags
  ['author', 'date-modified']

Function attributes are converted to tagged values when method
attribute definitions are created::

  >>> class IBazFactory(zope.interface.Interface):
  ...     def __call__():
  ...         "create one"
  ...     __call__.return_type = IBaz

  >>> IBazFactory['__call__'].getTaggedValue('return_type')
  <InterfaceClass __main__.IBaz>

Tagged values can also be defined from within an interface definition::

  >>> class IWithTaggedValues(zope.interface.Interface):
  ...     zope.interface.taggedValue('squish', 'squash')
  >>> IWithTaggedValues.getTaggedValue('squish')
  'squash'

Invariants
==========

Interfaces can express conditions that must hold for objects that
provide them. These conditions are expressed using one or more
invariants.  Invariants are callable objects that will be called with
an object that provides an interface. An invariant raises an `Invalid`
exception if the condition doesn't hold.  Here's an example::

  >>> class RangeError(zope.interface.Invalid):
  ...     """A range has invalid limits"""
  ...     def __repr__(self):
  ...         return "RangeError(%r)" % self.args

  >>> def range_invariant(ob):
  ...     if ob.max < ob.min:
  ...         raise RangeError(ob)

Given this invariant, we can use it in an interface definition::

  >>> class IRange(zope.interface.Interface):
  ...     min = zope.interface.Attribute("Lower bound")
  ...     max = zope.interface.Attribute("Upper bound")
  ...
  ...     zope.interface.invariant(range_invariant)

Interfaces have a method for checking their invariants::

  >>> class Range(object):
  ...     zope.interface.implements(IRange)
  ...
  ...     def __init__(self, min, max):
  ...         self.min, self.max = min, max
  ...
  ...     def __repr__(self):
  ...         return "Range(%s, %s)" % (self.min, self.max)

  >>> IRange.validateInvariants(Range(1,2))
  >>> IRange.validateInvariants(Range(1,1))
  >>> IRange.validateInvariants(Range(2,1))
  Traceback (most recent call last):
  ...
  RangeError: Range(2, 1)

If you have multiple invariants, you may not want to stop checking
after the first error.  If you pass a list to `validateInvariants`,
then a single `Invalid` exception will be raised with the list of
exceptions as it's argument::

  >>> from zope.interface.exceptions import Invalid
  >>> errors = []
  >>> try:
  ...     IRange.validateInvariants(Range(2,1), errors)
  ... except Invalid, e:
  ...     str(e)
  '[RangeError(Range(2, 1))]'
  
And the list will be filled with the individual exceptions::

  >>> errors
  [RangeError(Range(2, 1))]


  >>> del errors[:]

Adaptation
==========

Interfaces can be called to perform adaptation.

The semantics are based on those of the PEP 246 adapt function.

If an object cannot be adapted, then a TypeError is raised::

  >>> class I(zope.interface.Interface):
  ...     pass

  >>> I(0)
  Traceback (most recent call last):
  ...
  TypeError: ('Could not adapt', 0, <InterfaceClass __main__.I>)



unless an alternate value is provided as a second positional argument::

  >>> I(0, 'bob')
  'bob'

If an object already implements the interface, then it will be returned::

  >>> class C(object):
  ...     zope.interface.implements(I)

  >>> obj = C()
  >>> I(obj) is obj
  True

If an object implements __conform__, then it will be used::

  >>> class C(object):
  ...     zope.interface.implements(I)
  ...     def __conform__(self, proto):
  ...          return 0

  >>> I(C())
  0

Adapter hooks (see __adapt__) will also be used, if present::

  >>> from zope.interface.interface import adapter_hooks
  >>> def adapt_0_to_42(iface, obj):
  ...     if obj == 0:
  ...         return 42

  >>> adapter_hooks.append(adapt_0_to_42)
  >>> I(0)
  42

  >>> adapter_hooks.remove(adapt_0_to_42)
  >>> I(0)
  Traceback (most recent call last):
  ...
  TypeError: ('Could not adapt', 0, <InterfaceClass __main__.I>)

__adapt__
---------

  >>> class I(zope.interface.Interface):
  ...     pass

Interfaces implement the PEP 246 __adapt__ method.

This method is normally not called directly. It is called by the PEP
246 adapt framework and by the interface __call__ operator.

The adapt method is responsible for adapting an object to the
reciever.

The default version returns None::

  >>> I.__adapt__(0)

unless the object given provides the interface::

  >>> class C(object):
  ...     zope.interface.implements(I)

  >>> obj = C()
  >>> I.__adapt__(obj) is obj
  True

Adapter hooks can be provided (or removed) to provide custom
adaptation. We'll install a silly hook that adapts 0 to 42.
We install a hook by simply adding it to the adapter_hooks
list::

  >>> from zope.interface.interface import adapter_hooks
  >>> def adapt_0_to_42(iface, obj):
  ...     if obj == 0:
  ...         return 42

  >>> adapter_hooks.append(adapt_0_to_42)
  >>> I.__adapt__(0)
  42

Hooks must either return an adapter, or None if no adapter can
be found.

Hooks can be uninstalled by removing them from the list::

  >>> adapter_hooks.remove(adapt_0_to_42)
  >>> I.__adapt__(0)


.. [#create] The main reason we subclass `Interface` is to cause the
             Python class statement to create an interface, rather
             than a class.

             It's possible to create interfaces by calling a special
             interface class directly.  Doing this, it's possible
             (and, on rare occasions, useful) to create interfaces
             that don't descend from `Interface`.  Using this
             technique is beyond the scope of this document.

.. [#factory] Classes are factories.  They can be called to create
              their instances.  We expect that we will eventually
              extend the concept of implementation to other kinds of
              factories, so that we can declare the interfaces
              provided by the objects created.

.. [#compat] The goal is substitutability.  An object that provides an
             extending interface should be substitutable for an object
             that provides the extended interface.  In our example, an
             object that provides IBaz should be usable whereever an
             object that provides IBlat is expected.

             The interface implementation doesn't enforce this.
             but maybe it should do some checks.

================
Adapter Registry
================

Adapter registries provide a way to register objects that depend on
one or more interface specifications and provide (perhaps indirectly)
some interface.  In addition, the registrations have names. (You can
think of the names as qualifiers of the provided interfaces.)

The term "interface specification" refers both to interfaces and to
interface declarations, such as declarations of interfaces implemented
by a class.


Single Adapters
===============

Let's look at a simple example, using a single required specification::

  >>> from zope.interface.adapter import AdapterRegistry
  >>> import zope.interface

  >>> class IR1(zope.interface.Interface):
  ...     pass
  >>> class IP1(zope.interface.Interface):
  ...     pass
  >>> class IP2(IP1):
  ...     pass

  >>> registry = AdapterRegistry()

We'll register an object that depends on IR1 and "provides" IP2::

  >>> registry.register([IR1], IP2, '', 12)

Given the registration, we can look it up again::

  >>> registry.lookup([IR1], IP2, '')
  12

Note that we used an integer in the example.  In real applications,
one would use some objects that actually depend on or provide
interfaces. The registry doesn't care about what gets registered, so
we'll use integers and strings to keep the examples simple. There is
one exception.  Registering a value of None unregisters any
previously-registered value.

If an object depends on a specification, it can be looked up with a
specification that extends the specification that it depends on::

  >>> class IR2(IR1):
  ...     pass
  >>> registry.lookup([IR2], IP2, '')
  12

We can use a class implementation specification to look up the object::

  >>> class C2:
  ...     zope.interface.implements(IR2)

  >>> registry.lookup([zope.interface.implementedBy(C2)], IP2, '')
  12


and it can be looked up for interfaces that its provided interface
extends::

  >>> registry.lookup([IR1], IP1, '')
  12
  >>> registry.lookup([IR2], IP1, '')
  12

But if you require a specification that doesn't extend the specification the
object depends on, you won't get anything::

  >>> registry.lookup([zope.interface.Interface], IP1, '')

By the way, you can pass a default value to lookup::

  >>> registry.lookup([zope.interface.Interface], IP1, '', 42)
  42

If you try to get an interface the object doesn't provide, you also
won't get anything::

  >>> class IP3(IP2):
  ...     pass
  >>> registry.lookup([IR1], IP3, '')

You also won't get anything if you use the wrong name::

  >>> registry.lookup([IR1], IP1, 'bob')
  >>> registry.register([IR1], IP2, 'bob', "Bob's 12")
  >>> registry.lookup([IR1], IP1, 'bob')
  "Bob's 12"

You can leave the name off when doing a lookup::

  >>> registry.lookup([IR1], IP1)
  12

If we register an object that provides IP1::

  >>> registry.register([IR1], IP1, '', 11)

then that object will be prefered over O(12)::

  >>> registry.lookup([IR1], IP1, '')
  11

Also, if we register an object for IR2, then that will be prefered
when using IR2::

  >>> registry.register([IR2], IP1, '', 21)
  >>> registry.lookup([IR2], IP1, '')
  21

Finding out what, if anything, is registered
--------------------------------------------

We can ask if there is an adapter registered for a collection of
interfaces. This is different than lookup, because it looks for an
exact match.

  >>> print registry.registered([IR1], IP1)
  11

  >>> print registry.registered([IR1], IP2)
  12

  >>> print registry.registered([IR1], IP2, 'bob')
  Bob's 12
  

  >>> print registry.registered([IR2], IP1)
  21

  >>> print registry.registered([IR2], IP2)
  None

In the last example, None was returned because nothing was registered
exactly for the given interfaces.

lookup1
-------

Lookup of single adapters is common enough that there is a specialized
version of lookup that takes a single required interface::

  >>> registry.lookup1(IR2, IP1, '')
  21
  >>> registry.lookup1(IR2, IP1)
  21

Actual Adaptation
-----------------

The adapter registry is intended to support adaptation, where one
object that implements an interface is adapted to another object that
supports a different interface.  The adapter registry supports the
computation of adapters. In this case, we have to register adapter
factories::

   >>> class IR(zope.interface.Interface):
   ...     pass

   >>> class X:
   ...     zope.interface.implements(IR)
           
   >>> class Y:
   ...     zope.interface.implements(IP1)
   ...     def __init__(self, context):
   ...         self.context = context

  >>> registry.register([IR], IP1, '', Y)

In this case, we registered a class as the factory. Now we can call
`queryAdapter` to get the adapted object::

  >>> x = X()
  >>> y = registry.queryAdapter(x, IP1)
  >>> y.__class__.__name__
  'Y'
  >>> y.context is x
  True

We can register and lookup by name too::

  >>> class Y2(Y):
  ...     pass

  >>> registry.register([IR], IP1, 'bob', Y2)
  >>> y = registry.queryAdapter(x, IP1, 'bob')
  >>> y.__class__.__name__
  'Y2'
  >>> y.context is x
  True

When the adapter factory produces `None`, then this is treated as if no
adapter has been found. This allows us to prevent adaptation (when desired)
and let the adapter factory determine whether adaptation is possible based on
the state of the object being adapted.

  >>> def factory(context):
  ...     if context.name == 'object':
  ...         return 'adapter'
  ...     return None

  >>> class Object(object):
  ...     zope.interface.implements(IR)
  ...     name = 'object'

  >>> registry.register([IR], IP1, 'conditional', factory) 
  >>> obj = Object()
  >>> registry.queryAdapter(obj, IP1, 'conditional')
  'adapter'
  >>> obj.name = 'no object'
  >>> registry.queryAdapter(obj, IP1, 'conditional') is None
  True
  >>> registry.queryAdapter(obj, IP1, 'conditional', 'default')
  'default'

An alternate method that provides the same function as `queryAdapter()` is
`adapter_hook()`::

  >>> y = registry.adapter_hook(IP1, x)
  >>> y.__class__.__name__
  'Y'
  >>> y.context is x
  True
  >>> y = registry.adapter_hook(IP1, x, 'bob')
  >>> y.__class__.__name__
  'Y2'
  >>> y.context is x
  True

The `adapter_hook()` simply switches the order of the object and
interface arguments.  It is used to hook into the interface call
mechanism.


Default Adapters
----------------
  
Sometimes, you want to provide an adapter that will adapt anything.
For that, provide None as the required interface::

  >>> registry.register([None], IP1, '', 1)
  
then we can use that adapter for interfaces we don't have specific
adapters for::

  >>> class IQ(zope.interface.Interface):
  ...     pass
  >>> registry.lookup([IQ], IP1, '')
  1

Of course, specific adapters are still used when applicable::

  >>> registry.lookup([IR2], IP1, '')
  21

Class adapters
--------------

You can register adapters for class declarations, which is almost the
same as registering them for a class::

  >>> registry.register([zope.interface.implementedBy(C2)], IP1, '', 'C21')
  >>> registry.lookup([zope.interface.implementedBy(C2)], IP1, '')
  'C21'

Dict adapters
-------------

At some point it was impossible to register dictionary-based adapters due a
bug. Let's make sure this works now:

  >>> adapter = {}
  >>> registry.register((), IQ, '', adapter)
  >>> registry.lookup((), IQ, '') is adapter
  True

Unregistering
-------------

You can unregister by registering None, rather than an object::

  >>> registry.register([zope.interface.implementedBy(C2)], IP1, '', None)
  >>> registry.lookup([zope.interface.implementedBy(C2)], IP1, '')
  21

Of course, this means that None can't be registered. This is an
exception to the statement, made earlier, that the registry doesn't
care what gets registered.

Multi-adapters
==============

You can adapt multiple specifications::

  >>> registry.register([IR1, IQ], IP2, '', '1q2')
  >>> registry.lookup([IR1, IQ], IP2, '')
  '1q2'
  >>> registry.lookup([IR2, IQ], IP1, '')
  '1q2'

  >>> class IS(zope.interface.Interface):
  ...     pass
  >>> registry.lookup([IR2, IS], IP1, '')

  >>> class IQ2(IQ):
  ...     pass

  >>> registry.lookup([IR2, IQ2], IP1, '')
  '1q2'

  >>> registry.register([IR1, IQ2], IP2, '', '1q22')
  >>> registry.lookup([IR2, IQ2], IP1, '')
  '1q22'

Multi-adaptation
----------------

You can adapt multiple objects::

  >>> class Q:
  ...     zope.interface.implements(IQ)

As with single adapters, we register a factory, which is often a class::

  >>> class IM(zope.interface.Interface):
  ...     pass
  >>> class M:
  ...     zope.interface.implements(IM)
  ...     def __init__(self, x, q):
  ...         self.x, self.q = x, q
  >>> registry.register([IR, IQ], IM, '', M)

And then we can call `queryMultiAdapter` to compute an adapter::

  >>> q = Q()
  >>> m = registry.queryMultiAdapter((x, q), IM)
  >>> m.__class__.__name__
  'M'
  >>> m.x is x and m.q is q
  True

and, of course, we can use names::

  >>> class M2(M):
  ...     pass
  >>> registry.register([IR, IQ], IM, 'bob', M2)
  >>> m = registry.queryMultiAdapter((x, q), IM, 'bob')
  >>> m.__class__.__name__
  'M2'
  >>> m.x is x and m.q is q
  True
  
Default Adapters
----------------

As with single adapters, you can define default adapters by specifying
None for the *first* specification::

  >>> registry.register([None, IQ], IP2, '', 'q2')
  >>> registry.lookup([IS, IQ], IP2, '')
  'q2'

Null Adapters
=============

You can also adapt no specification::

  >>> registry.register([], IP2, '', 2)
  >>> registry.lookup([], IP2, '')
  2
  >>> registry.lookup([], IP1, '')
  2

Listing named adapters
----------------------

Adapters are named. Sometimes, it's useful to get all of the named
adapters for given interfaces::

  >>> adapters = list(registry.lookupAll([IR1], IP1))
  >>> adapters.sort()
  >>> assert adapters == [(u'', 11), (u'bob', "Bob's 12")]

This works for multi-adapters too::

  >>> registry.register([IR1, IQ2], IP2, 'bob', '1q2 for bob')
  >>> adapters = list(registry.lookupAll([IR2, IQ2], IP1))
  >>> adapters.sort()
  >>> assert adapters == [(u'', '1q22'), (u'bob', '1q2 for bob')]

And even null adapters::

  >>> registry.register([], IP2, 'bob', 3)
  >>> adapters = list(registry.lookupAll([], IP1))
  >>> adapters.sort()
  >>> assert adapters == [(u'', 2), (u'bob', 3)]

Subscriptions
=============

Normally, we want to look up an object that most-closely matches a
specification.  Sometimes, we want to get all of the objects that
match some specification.  We use subscriptions for this.  We
subscribe objects against specifications and then later find all of
the subscribed objects::

  >>> registry.subscribe([IR1], IP2, 'sub12 1')
  >>> registry.subscriptions([IR1], IP2)
  ['sub12 1']

Note that, unlike regular adapters, subscriptions are unnamed.

You can have multiple subscribers for the same specification::

  >>> registry.subscribe([IR1], IP2, 'sub12 2')
  >>> registry.subscriptions([IR1], IP2)
  ['sub12 1', 'sub12 2']

If subscribers are registered for the same required interfaces, they
are returned in the order of definition.

You can register subscribers for all specifications using None::

  >>> registry.subscribe([None], IP1, 'sub_1')
  >>> registry.subscriptions([IR2], IP1)
  ['sub_1', 'sub12 1', 'sub12 2']

Note that the new subscriber is returned first.  Subscribers defined
for less general required interfaces are returned before subscribers
for more general interfaces.

Subscriptions may be combined over multiple compatible specifications::

  >>> registry.subscriptions([IR2], IP1)
  ['sub_1', 'sub12 1', 'sub12 2']
  >>> registry.subscribe([IR1], IP1, 'sub11')
  >>> registry.subscriptions([IR2], IP1)
  ['sub_1', 'sub12 1', 'sub12 2', 'sub11']
  >>> registry.subscribe([IR2], IP2, 'sub22')
  >>> registry.subscriptions([IR2], IP1)
  ['sub_1', 'sub12 1', 'sub12 2', 'sub11', 'sub22']
  >>> registry.subscriptions([IR2], IP2)
  ['sub12 1', 'sub12 2', 'sub22']

Subscriptions can be on multiple specifications::

  >>> registry.subscribe([IR1, IQ], IP2, 'sub1q2')
  >>> registry.subscriptions([IR1, IQ], IP2)
  ['sub1q2']
  
As with single subscriptions and non-subscription adapters, you can
specify None for the first required interface, to specify a default::

  >>> registry.subscribe([None, IQ], IP2, 'sub_q2')
  >>> registry.subscriptions([IS, IQ], IP2)
  ['sub_q2']
  >>> registry.subscriptions([IR1, IQ], IP2)
  ['sub_q2', 'sub1q2']

You can have subscriptions that are indepenent of any specifications::
  
  >>> list(registry.subscriptions([], IP1))
  []

  >>> registry.subscribe([], IP2, 'sub2')
  >>> registry.subscriptions([], IP1)
  ['sub2']
  >>> registry.subscribe([], IP1, 'sub1')
  >>> registry.subscriptions([], IP1)
  ['sub2', 'sub1']
  >>> registry.subscriptions([], IP2)
  ['sub2']

Unregistering subscribers
-------------------------

We can unregister subscribers.  When unregistering a subscriber, we
can unregister a specific subscriber::

  >>> registry.unsubscribe([IR1], IP1, 'sub11')
  >>> registry.subscriptions([IR1], IP1)
  ['sub_1', 'sub12 1', 'sub12 2']

If we don't specify a value, then all subscribers matching the given
interfaces will be unsubscribed:

  >>> registry.unsubscribe([IR1], IP2)
  >>> registry.subscriptions([IR1], IP1)
  ['sub_1']


Subscription adapters
---------------------

We normally register adapter factories, which then allow us to compute
adapters, but with subscriptions, we get multiple adapters.  Here's an
example of multiple-object subscribers::

  >>> registry.subscribe([IR, IQ], IM, M)
  >>> registry.subscribe([IR, IQ], IM, M2)

  >>> subscribers = registry.subscribers((x, q), IM)
  >>> len(subscribers)
  2
  >>> class_names = [s.__class__.__name__ for s in subscribers]
  >>> class_names.sort()
  >>> class_names
  ['M', 'M2']
  >>> [(s.x is x and s.q is q) for s in subscribers]
  [True, True]

adapter factory subcribers can't return None values::

  >>> def M3(x, y):
  ...     return None

  >>> registry.subscribe([IR, IQ], IM, M3)
  >>> subscribers = registry.subscribers((x, q), IM)
  >>> len(subscribers)
  2

Handlers
--------

A handler is a subscriber factory that doesn't produce any normal
output.  It returns None.  A handler is unlike adapters in that it does
all of its work when the factory is called.

To register a handler, simply provide None as the provided interface::

  >>> def handler(event):
  ...     print 'handler', event

  >>> registry.subscribe([IR1], None, handler)
  >>> registry.subscriptions([IR1], None) == [handler]
  True

==========================
Using the Adapter Registry
==========================

This is a small demonstration of the ``zope.interface`` package including its
adapter registry. It is intended to provide a concrete but narrow example on
how to use interfaces and adapters outside of Zope 3.

First we have to import the interface package::

  >>> import zope.interface

We now develop an interface for our object, which is a simple file in this
case. For now we simply support one attribute, the body, which contains the
actual file contents::

  >>> class IFile(zope.interface.Interface):
  ...
  ...     body = zope.interface.Attribute('Contents of the file.')
  ...

For statistical reasons we often want to know the size of a file. However, it
would be clumsy to implement the size directly in the file object, since the
size really represents meta-data. Thus we create another interface that
provides the size of something::

  >>> class ISize(zope.interface.Interface):
  ...
  ...     def getSize():
  ...         'Return the size of an object.'
  ...

Now we need to implement the file. It is essential that the object states
that it implements the `IFile` interface. We also provide a default body
value (just to make things simpler for this example)::

  >>> class File(object):
  ...
  ...      zope.interface.implements(IFile)
  ...      body = 'foo bar'
  ...

Next we implement an adapter that can provide the `ISize` interface given any
object providing `IFile`. By convention we use `__used_for__` to specify the
interface that we expect the adapted object to provide, in our case
`IFile`. However, this attribute is not used for anything. If you have
multiple interfaces for which an adapter is used, just specify the interfaces
via a tuple.

Again by convention, the constructor of an adapter takes one argument, the
context. The context in this case is an instance of `File` (providing `IFile`)
that is used to extract the size from. Also by convention the context is
stored in an attribute named `context` on the adapter. The twisted community
refers to the context as the `original` object. However, you may feel free to
use a specific argument name, such as `file`::

  >>> class FileSize(object):
  ...
  ...      zope.interface.implements(ISize)
  ...      __used_for__ = IFile
  ...
  ...      def __init__(self, context):
  ...          self.context = context
  ...
  ...      def getSize(self):
  ...          return len(self.context.body)
  ...

Now that we have written our adapter, we have to register it with an adapter
registry, so that it can be looked up when needed. There is no such thing as a
global registry; thus we have to instantiate one for our example manually::

  >>> from zope.interface.adapter import AdapterRegistry
  >>> registry = AdapterRegistry()


The registry keeps a map of what adapters implement based on another
interface, the object already provides. Therefore, we next have to register an
adapter that adapts from `IFile` to `ISize`. The first argument to
the registry's `register()` method is a list of original interfaces.In our
cause we have only one original interface, `IFile`. A list makes sense, since
the interface package has the concept of multi-adapters, which are adapters
that require multiple objects to adapt to a new interface. In these
situations, your adapter constructor will require an argument for each
specified interface.

The second argument is the interface the adapter provides, in our case
`ISize`. The third argument is the name of the adapter. Since we do not care
about names, we simply leave it as an empty string. Names are commonly useful,
if you have adapters for the same set of interfaces, but they are useful in
different situations. The last argument is simply the adapter class::

  >>> registry.register([IFile], ISize, '', FileSize)

You can now use the the registry to lookup the adapter::

  >>> registry.lookup1(IFile, ISize, '')
  <class '__main__.FileSize'>

Let's get a little bit more practical. Let's create a `File` instance and
create the adapter using a registry lookup. Then we see whether the adapter
returns the correct size by calling `getSize()`::

  >>> file = File()
  >>> size = registry.lookup1(IFile, ISize, '')(file)
  >>> size.getSize()
  7

However, this is not very practical, since I have to manually pass in the
arguments to the lookup method. There is some syntactic candy that will allow
us to get an adapter instance by simply calling `ISize(file)`. To make use of
this functionality, we need to add our registry to the adapter_hooks list,
which is a member of the adapters module. This list stores a collection of
callables that are automatically invoked when IFoo(obj) is called; their
purpose is to locate adapters that implement an interface for a certain
context instance.

You are required to implement your own adapter hook; this example covers one
of the simplest hooks that use the registry, but you could implement one that
used an adapter cache or persistent adapters, for instance. The helper hook is
required to expect as first argument the desired output interface (for us
`ISize`) and as the second argument the context of the adapter (here
`file`). The function returns an adapter, i.e. a `FileSize` instance::

  >>> def hook(provided, object):
  ...     adapter = registry.lookup1(zope.interface.providedBy(object),
  ...                                provided, '')
  ...     return adapter(object)
  ...

We now just add the hook to an `adapter_hooks` list::

  >>> from zope.interface.interface import adapter_hooks
  >>> adapter_hooks.append(hook)

Once the hook is registered, you can use the desired syntax::

  >>> size = ISize(file)
  >>> size.getSize()
  7

Now we have to cleanup after ourselves, so that others after us have a clean
`adapter_hooks` list::

  >>> adapter_hooks.remove(hook)

That's it. I have intentionally left out a discussion of named adapters and
multi-adapters, since this text is intended as a practical and simple
introduction to Zope 3 interfaces and adapters. You might want to read the
`adapter.txt` in the `zope.interface` package for a more formal, referencial
and complete treatment of the package. Warning: People have reported that
`adapter.txt` makes their brain feel soft!

CHANGES
*******

==================
3.6.1 (2010-05-03)
==================

- A non-ascii character in the changelog made 3.6.0 uninstallable on Python 3 systems 
  with another default encoding than UTF-8.

- Fixed compiler warnings under GCC 4.3.3.

==================
3.6.0 (2010-04-29)
==================

- LP #185974:  Clear the cache used by ``Specificaton.get`` inside
  ``Specification.changed``.  Thanks to Jacob Holm for the patch.

- Added support for Python 3.1. Contributors:

    Lennart Regebro
    Martin v Loewis
    Thomas Lotze
    Wolfgang Schnerring

  The 3.1 support is completely backwards compatible. However, the implements
  syntax used under Python 2.X does not work under 3.X, since it depends on
  how metaclasses are implemented and this has changed. Instead it now supports
  a decorator syntax (also under Python 2.X)::

    class Foo:
        implements(IFoo)
        ...

  can now also be written::

    @implementor(IFoo):
    class Foo:
        ...

  There are 2to3 fixers available to do this change automatically in the
  zope.fixers package.

- Python 2.3 is no longer supported.


==================
3.5.4 (2009-12-23)
==================

- Use the standard Python doctest module instead of zope.testing.doctest, which
  has been deprecated.


==================
3.5.3 (2009-12-08)
==================

- Fix an edge case: make providedBy() work when a class has '__provides__' in
  its __slots__ (see http://thread.gmane.org/gmane.comp.web.zope.devel/22490)


==================
3.5.2 (2009-07-01)
==================

- BaseAdapterRegistry.unregister, unsubscribe: Remove empty portions of
  the data structures when something is removed.  This avoids leaving
  references to global objects (interfaces) that may be slated for
  removal from the calling application.


==================
3.5.1 (2009-03-18)
==================

- verifyObject: use getattr instead of hasattr to test for object attributes
  in order to let exceptions other than AttributeError raised by properties
  propagate to the caller

- Add Sphinx-based documentation building to the package buildout
  configuration. Use the ``bin/docs`` command after buildout.

- Improve package description a bit. Unify changelog entries formatting.

- Change package's mailing list address to zope-dev at zope.org as
  zope3-dev at zope.org is now retired.


==================
3.5.0 (2008-10-26)
==================

- Fixed declaration of _zope_interface_coptimizations, it's not a top level
  package.

- Add a DocTestSuite for odd.py module, so their tests are run.

- Allow to bootstrap on Jython.

- Fix https://bugs.launchpad.net/zope3/3.3/+bug/98388: ISpecification
  was missing a declaration for __iro__.

- Added optional code optimizations support, which allows the building
  of C code optimizations to fail (Jython).

- Replaced `_flatten` with a non-recursive implementation, effectively making
  it 3x faster.


==================
3.4.1 (2007-10-02)
==================

- Fixed a setup bug that prevented installation from source on systems
  without setuptools.


==================
3.4.0 (2007-07-19)
==================

- Final release for 3.4.0.


====================
3.4.0b3 (2007-05-22)
====================


- Objects with picky custom comparison methods couldn't be added to
  component registries.  Now, when checking whether an object is
  already registered, identity comparison is used.


====================
3.3.0.1 (2007-01-03)
====================

- Made a reference to OverflowWarning, which disappeared in Python
  2.5, conditional.


==================
3.3.0 (2007/01/03)
==================

New Features
============

- The adapter-lookup algorithim was refactored to make it
  much simpler and faster.  

  Also, more of the adapter-lookup logic is implemented in C, making
  debugging of application code easier, since there is less
  infrastructre code to step through.

- We now treat objects without interface declarations as if they
  declared that they provide zope.interface.Interface.

- There are a number of richer new adapter-registration interfaces
  that provide greater control and introspection.

- Added a new interface decorator to zope.interface that allows the
  setting of tagged values on an interface at definition time (see
  zope.interface.taggedValue).

Bug Fixes
=========

- A bug in multi-adapter lookup sometimes caused incorrect adapters to
  be returned.


====================
3.2.0.2 (2006-04-15)
====================

- Fix packaging bug:  'package_dir' must be a *relative* path.


====================
3.2.0.1 (2006-04-14)
====================

- Packaging change:  suppress inclusion of 'setup.cfg' in 'sdist' builds.


==================
3.2.0 (2006-01-05)
==================

- Corresponds to the verison of the zope.interface package shipped as part of
  the Zope 3.2.0 release.


==================
3.1.0 (2005-10-03)
==================

- Corresponds to the verison of the zope.interface package shipped as part of
  the Zope 3.1.0 release.

- Made attribute resolution order consistent with component lookup order,
  i.e. new-style class MRO semantics.

- Deprecated 'isImplementedBy' and 'isImplementedByInstancesOf' APIs in
  favor of 'implementedBy' and 'providedBy'.


==================
3.0.1 (2005-07-27)
==================

- Corresponds to the verison of the zope.interface package shipped as part of
  the Zope X3.0.1 release.

- Fixed a bug reported by James Knight, which caused adapter registries
  to fail occasionally to reflect declaration changes.


==================
3.0.0 (2004-11-07)
==================

- Corresponds to the verison of the zope.interface package shipped as part of
  the Zope X3.0.0 release.

Download
********


%prep
%setup -n zope.interface-3.6.1

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
