"""Provides constants used by the utillity package."""

# net/http in Golang responds with the following when sent an HTTP request to a port
# expecting HTTPS.
#
# String taken from serve() in src/net/http/server.go.
#
WRONG_TRANSPORT_GO_NET_HTTP = b"Client sent an HTTP request to an HTTPS server."

# Apache Tomcat responds with the following when sent an HTTP request to a port
# expecting HTTPS.
#
# String taken from java/org/apache/tomcat/util/net/TLSClientHelloExtractor.java
#
WRONG_TRANSPORT_TOMCAT = b"This combination of host and port requires TLS."

# "Wrong transport" messages are from services which respond to HTTP requests on ports
# expecting HTTPS. This confuses scheme detection, as some servers that receive an HTTP
# request to a port expecting HTTPS will return a well formed response containing one of
# the following messages, rather than an error.
WRONG_TRANSPORT = [WRONG_TRANSPORT_TOMCAT, WRONG_TRANSPORT_GO_NET_HTTP]

# Define supported protocol schemes for lookup ane enumeration functions.
PROTOCOL_SCHEME_HTTP = "http"
PROTOCOL_SCHEME_HTTPS = "https"

PROTOCOL_SCHEMES = [PROTOCOL_SCHEME_HTTP, PROTOCOL_SCHEME_HTTPS]
