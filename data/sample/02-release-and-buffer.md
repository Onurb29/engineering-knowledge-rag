# Release work at the bottleneck's pace

If jobs enter the line faster than the bottleneck can process them, the queue grows. An upstream station with spare capacity can run faster briefly to refill a buffer, then slow down.

## What a buffer protects

A small queue of ready jobs can keep Assembly working through short interruptions upstream. The buffer protects Assembly from running out of work. Assembly's sustained capacity still sets how fast it can finish units.
