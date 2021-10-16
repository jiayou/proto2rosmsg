# proto2rosmsg

convert proto file to ROS messages.

```
python3 proto2rosmsg proto_example/modules/canbus/proto/chassis.proto
```

```
find proto_example -name '*.proto' | xargs -n1 python3 proto2rosmsg
```

# limitations
- only proto2 syntax is supported
- empty message is not supported, e.g.
```
message Foo {}
```
- signal should be in one line
```
required float abc = 1;	// ok

required float
  abc = 1;		// not ok

```
- variant types (e.g. oneof) are not supported
- gprc service is not supported
- map is not supported, e.g.
```
map<string, bool> foo = 1;
```
