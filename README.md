
# a server of mingrammer/diagrams

## RUN

```
docker run --rm -d -p 8080:80 tamuto/diagrams-server
```

## BUILD

```
docker build -t diagrams-server .
```

## Example

display as a image.

```
<img src='http://localhost:8080/?
with Diagram("Grouped Workers", show=False, direction="TB"):
    ELB("lb") >> [EC2("worker1"),
                  EC2("worker2"),
                  EC2("worker3"),
                  EC2("worker4"),
                  EC2("worker5")] >> RDS("events")
'>
```

## Caution

Do not publish the server on the Internet.
This server have some security hole.
