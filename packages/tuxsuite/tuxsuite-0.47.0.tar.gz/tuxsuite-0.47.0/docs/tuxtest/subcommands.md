# Sub-commands

## get

`get` is a subcommand which fetches the details for the test
identified by its `uid`.

```
tuxsuite test get 1t2giSA1sSKFADKPrl0YI1gjMLb
```

## list

`list` is a subcommand which fetches the latest 30 tests by default.

```
tuxsuite test list
```

In order to restrict the number of tests fetched, `--limit` is used
as follows:

```
tuxsuite test list --limit 5
```

To get the output of the above commands in JSON format, use the
following:

```
tuxsuite test list --json --limit 2
```

## logs

`logs` is a subcommand which fetches the log for the test identified
by its `uid`.

```
tuxsuite test logs 1t2giSA1sSKFADKPrl0YI1gjMLb
```

In order to fetch the logs in raw format use the following option:

```
tuxsuite test logs 1t2giSA1sSKFADKPrl0YI1gjMLb --raw
```

## results

`results` is a subcommand which fetches the results for the test
identified by its `uid`.

```
tuxsuite test results 1t2giSA1sSKFADKPrl0YI1gjMLb
```

In order to fetch the results in raw format use the following option:

```
tuxsuite test results 1t2giSA1sSKFADKPrl0YI1gjMLb --raw
```

## wait

`wait` is a subcommand which fetches the details for the test
identified by its `uid`, if the test is in progress, it will update
the details on screen. This will be handy to submit a test and come
back at a later point of time to watch the test's progression.

```
tuxsuite test wait 1t2giSA1sSKFADKPrl0YI1gjMLb
```
