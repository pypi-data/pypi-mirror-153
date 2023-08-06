import re

SentryDSN = "https://34647c66cad04a51b814cfade7b8d110@o373009.ingest.sentry.io/5342537"
SegmentWriteKey = "4RrqDnVYxMTE8wYJDNWKaPjHCSn9egeY"

AwsOktaNoRoles = re.compile("There are no roles that can be assumed|ARN isn't valid")
AwsOktaNotSetup = re.compile("404 Not Found")
AwsOktaNoCreds = re.compile("Okta credentials are not in your keyring")

Saml2AwsNoRoles = re.compile(
    "no (?:account|role)s available|Supplied RoleArn not found in saml assertion"
)
Saml2AwsNoCreds = re.compile("aws credentials not found")
Saml2AwsCredsExpired = re.compile("aws credentials have expired")
