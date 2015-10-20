# Open IE 4.0
Open IE 4.0 is the successor to Ollie system.
for more information check the project's [Github repository](https://github.com/knowitall/openie)


Note : for github constraints of having large files (openie 4.0 jar is 800m)
please download the project / compile and create the jar file yourself
through executing the following command lines (execute from this path)

```
wget https://github.com/knowitall/openie/zipball/master
sbt -J-Xmx2700M clean compile assembly

# you will fine the jar file inside /target folder

mv  /path/to/jar-file-name.jar  ./openie-4.0.jar

find ! -name 'openie-4.0.jar' -type d -exec rm -rf {} +   #remove all other files except the jar

# to run the OpenIE-4.0 jar file run :
java -Xmx4g -XX:+UseConcMarkSweepGC -jar openie-4.0.jar
```
