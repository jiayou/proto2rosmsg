# proto2rosmsg

convert proto file to ROS messages.

```
python3 proto2rosmsg.py proto_example/modules/canbus/proto/chassis.proto
```

```
find proto_example -name '*.proto' | xargs -n1 python3 proto2rosmsg.py
```

# limitations
- only proto2 syntax is supported
- enum is treated as int32 (defined in enum_list.txt)
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

# generate enumeration list
```
find proto_example -name *.proto | xargs grep -h "enum " | sed 's/^[ \t]*//g' | grep ^enum | sed 's/{//g' | awk '{print $2}' | sort | uniq > enum_list.txt
```
