"""Provides common JupiterOne queries."""

# Returns all running GCP Compute Instances which permits traffic inbound from the
# internet - using a protocol of TCP or 'ALL'.
INTERNET_LISTENERS_GCP_COMPUTE = """
  FIND google_compute_instance AS i
  THAT HAS google_compute_subnetwork
  THAT CONTAINS google_compute_network
  THAT PROTECTS google_compute_firewall
  THAT ALLOWS Internet
 WHERE (i.status != 'TERMINATED' AND i.status != 'STOPPED')
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='all')
   AND i.publicIpAddress != undefined
RETURN
    i.id AS id,
    i._type AS type,
    i.zone AS location,
    i.displayName AS name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.publicIpAddress AS address,
    i.projectId,
    i.status,
    i.serviceAccountEmails,
    i.tag.AccountName
"""

# Returns all running AWS EC2 Instances which permit traffic inbound from the internet -
# using a protocol of TCP or 'ALL' ('*').
INTERNET_LISTENERS_AWS_EC2 = """
  FIND aws_instance
  WITH state != 'stopped'
   AND state != 'terminated'
   AND publicIpAddress != undefined AS i
  THAT PROTECTS aws_security_group
  THAT ALLOWS Internet
 WHERE ALLOWS.ingress=true
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='*')
RETURN
    i.instanceId AS id,
    i._type AS type,
    i.region AS location,
    i.name AS name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.publicIpAddress AS address,
    i.launchTime,
    i.ownerId,
    ALLOWS.ipProtocol
"""

# Returns all running Azure VMs which permit traffic inbound from the internet - using
# a protocol of TCP or 'ALL'.
INTERNET_LISTENERS_AZURE_VM = """
  FIND azure_vm
  WITH state != "stopped" AS i
  THAT USES azure_nic as n
  THAT PROTECTS azure_security_group
  THAT ALLOWS Internet
 WHERE n.publicIp != undefined
   AND ALLOWS.direction = "Inbound"
   AND (ALLOWS.ipProtocol = 'tcp' OR ALLOWS.ipProtocol='all')
RETURN
    i.vmId AS id,
    i._type AS type,
    i.region AS location,
    i.name as name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    n.publicIp AS address,
    i.id,
    i.platform
"""

# Returns all AWS ALBs which permit traffic inbound from the internet - using a protocol
# of TCP or 'ALL' ('*').
INTERNET_LISTENERS_AWS_ALB = """
  FIND aws_alb
  WITH scheme = 'internet-facing' as i
  THAT PROTECTS aws_security_group
  THAT ALLOWS Internet
 WHERE ALLOWS.ingress=true
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='*')
RETURN
    i.arn as id,
    i._type as type,
    i.region AS location,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.dnsName as address,
    i.ownerId,
    ALLOWS.ipProtocol
"""

# Returns all AWS ELBs which permit traffic inbound from the internet - using a protocol
# of TCP or 'ALL' ('*').
INTERNET_LISTENERS_AWS_ELB = """
  FIND aws_alb
  WITH scheme = 'internet-facing' as i
  THAT PROTECTS aws_security_group
  THAT ALLOWS Internet
 WHERE ALLOWS.ingress=true
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='*')
RETURN
    i.arn as id,
    i._type as type,
    i.region AS location,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.dnsName as address,
    i.ownerId,
    ALLOWS.ipProtocol
"""

# Returns all AWS NLBs which have instances associated that permit traffic inbound from
# the internet - using a protocol of TCP or 'ALL' ('*').
INTERNET_LISTENERS_AWS_NLB = """
  FIND aws_nlb
  WITH scheme = 'internet-facing' AS i
  THAT CONNECTS aws_lb_target_group
  THAT HAS aws_instance
  THAT PROTECTS aws_security_group
  THAT ALLOWS Internet
 WHERE ALLOWS.ingress=true
   AND (ALLOWS.ipProtocol='tcp' OR ALLOWS.ipProtocol='*')
RETURN
    i.arn as id,
    i._type as type,
    i.region AS location,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    i.dnsName as address,
    i.ownerId,
    ALLOWS.ipProtocol
"""

# Returns all Azure Load Balancers which permit traffic inbound from the internet -
# using a protocol of TCP or 'ALL'.
INTERNET_LISTENERS_AZURE_LB = """
  FIND azure_lb WITH public = true AS i
  THAT CONNECTS azure_nic as n
  THAT PROTECTS azure_security_group
  THAT ALLOWS Internet
 WHERE n.publicIp != undefined
   AND ALLOWS.direction = "Inbound"
   AND (ALLOWS.ipProtocol = 'tcp' OR ALLOWS.ipProtocol='all')
RETURN
    i.vmId AS id,
    i._type AS type,
    i.region AS location,
    i.name as name,
    ALLOWS.toPort AS to_port,
    ALLOWS.fromPort AS from_port,
    n.publicIp AS address,
    i.id,
    i.platform
"""

# Returns all GCP URL Maps which permit traffic inbound from the internet - using a
# protocol of TCP or 'ALL'.
#
# TODO: Decipher the magic spell to map a google_compute_forwarding_rule all the way
#       back to a backend, including respective / relevant firewall entries.
#
