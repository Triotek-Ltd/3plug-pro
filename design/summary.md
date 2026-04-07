# 3plug Summary

## Short answer

Yes.

Triotek can customize its Frappe/Bench operational model, use its own repositories, define its own workflows, and build a UI-driven platform called `3plug` to manage those actions.

## What 3plug is meant to do

3plug is meant to sit above Bench and turn it into a managed platform capability.

That means:

* UI for operators
* API for actions
* job system for execution
* audit history for accountability
* support for Triotek repos and app stacks
* backup, restore, deploy, and migration workflows

## Can it replace Press?

Yes, if Triotek builds the control-plane features Press normally gives:

* environment management
* site lifecycle management
* app deployment management
* backups and restores
* visibility and auditability
* operational permissions

## Can it replace Docker workflows?

Partly or fully, depending on the runtime model.

3plug can replace the operational layer that currently depends on shell scripts or container routines, but the underlying infrastructure still needs to exist somewhere.

So the real model is:

* Bench is the execution engine
* 3plug is the control plane
* runtime may still be native, containerized, or hybrid

## Best practical approach

Do not start by deeply forking Bench.

Start by:

* wrapping Bench safely
* controlling actions through jobs
* using Triotek repos
* building clear environment and site state
* adding auditability and permissions

That path gets Triotek a platform without creating unnecessary upstream maintenance pain too early.

## Documents in this folder

* [architecture.md](architecture.md)
* [scope.md](scope.md)
