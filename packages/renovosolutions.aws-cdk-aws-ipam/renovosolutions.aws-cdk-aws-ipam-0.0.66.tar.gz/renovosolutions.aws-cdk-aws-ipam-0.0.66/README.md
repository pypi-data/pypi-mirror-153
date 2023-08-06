# AWS ELBv2 Redirection CDK Construct Library

This library makes it easy to creation redirection rules on Application Load Balancers.

## Usage

### Base redirection construct (Typescript)

```python
// create a vpc
const vpc = new ec2.Vpc(stack, 'vpc');

// create an alb in that vpc
const alb = new elbv2.ApplicationLoadBalancer(stack, 'alb', {
  internetFacing: true,
  vpc,
});

// create a redirect from 8080 to 8443
new Redirect(stack, 'redirect', {
  alb,
  sourcePort: 8080,
  sourceProtocol: elbv2.ApplicationProtocol.HTTP,
  targetPort: 8443,
  targetProtocol: elbv2.ApplicationProtocol.HTTPS,
});
```

### Using the pre-build HTTP to HTTPS construct (Typescript)

```python
// create a vpc
const vpc = new ec2.Vpc(stack, 'vpc');

// create an alb in that vpc
const alb = new elbv2.ApplicationLoadBalancer(stack, 'alb', {
  internetFacing: true,
  vpc,
});

// use the pre-built construct for HTTP to HTTPS
new RedirectHttpHttps(stack, 'redirectHttpHttps', {
  alb,
});
```
