======================================================
[Numpy-discussion] problem with assigning to recarrays
======================================================
>
> On Feb 27, 2009, at 4:30 PM, Robert Kern wrote:
>>>
>> r[where(r.field1 == 1.)] make a copy. There is no way for us to
>> construct a view onto the original memory for this circumstance given
>> numpy's memory model.
>
> Many thanks for the quick reply.  I assume that this is true only for
> record arrays, not for ordinary arrays?  Certainly I can make an
> assignment in this way with a normal array.

Well, you are doing two very different things. Let's back up a bit.

Python gives us two hooks to modify an object in-place with an
assignment: __setitem__ and __setattr__.

  x[<item>] = y   ==>  x.__setitem__(<item>, y)
  x.<attr>  = y   ==>  x.__setattr__('<attr>', y)

Now, we don't need to restrict ourselves to just variables for 'x'; we
can have any expression that evaluates to an object.

  (<expr>)[<item>] = y  ==> (<expr>).__setitem__(<item>, y)
  (<expr>).<attr>  = y  ==> (<expr>).__setattr__('<attr>', y)

The key here is that the (<expr>) on the LHS is evaluated just like
any expression appearing anywhere else in your code. The only special
in-place behavior is restricted to the *outermost* [<item>] or
.<attr>.

So when you do this:

  r[where(r.field1 == 1.)].field2 = 1.0

it translates to something like this:

  tmp = r.__getitem__(where(r.field1 == 1.0))  # Makes a copy!
  tmp.__setattr__('field2', 1.0)

Note that the first line is a __getitem__, not a __setitem__ which can
modify r in-place.

> Also, if it is truly impossible to change this behavior, or to have it
> raise an error--then are there any best-practice suggestions for how
> to remember and avoid running into this non-obvious behavior?  If one
> thinks of record arrays as inheriting  from numpy arrays, then this
> problem is certainly unexpected.

It's a natural consequence of the preceding rules. This a Python
thing, not a difference between numpy arrays and record arrays. Just
keep those rules in mind.

> Also, I've just found that the following syntax does do what is
> expected:
>
> (r.field2)[where(field1 == 1.)] = 1.
>
> It is at least a little aesthetically displeasing that the syntax
> works one way but not the other.  Perhaps my best bet is to stick with
> this syntax and forget that the other exists?  A less-than-satisfying
> solution, but workable.

If you drop the extraneous bits, it becomes a fair bit more readable:

  r.field2[r.field1 == 1] = 1

This is idiomatic; you'll see it all over the place where record
arrays are used. The reason that this form modifies r in-place is
because r.__getattr__('field2') is able to return a view rather than a
copy.

-- 
Robert Kern
