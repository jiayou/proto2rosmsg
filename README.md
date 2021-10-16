# proto2rosmsg

convert proto file to ROS messages.

```
python3 proto2rosmsg proto_example/modules/canbus/proto/chassis.proto
```

```
find proto_examples -name '*.proto' | xargs -n1 python3 proto2rosmsg
```

# limits
- only proto2 is supported
- nested message is not supported, e.g.
```
message A{
  message B{
    required foo = 1;
  }
  ...
}

```
- empty message is not supported, e.g.
```
message Foo {}
```
- signal in one line
```
required float abc = 1;	// ok

required float
  abc = 1;		// not ok

```
- variant types (oneof, anyof) are not supported
- gprc service is not supported
- map is not supported, e.g.
```
map<string, bool> foo = 1;
```
