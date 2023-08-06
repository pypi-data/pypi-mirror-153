# cdk-lex-zip-import

![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

An AWS Cloud Development Kit (AWS CDK) construct library that allows you to upload and deploy a Zipped Lex Bot. Once imported, this Bot can be managed within the Amazon Lex Console.

## Usage

To add to your AWS CDK package.json file:

```
yarn add cdk-lex-zip-import
```

Within your AWS CDK:

### Import Lex Bot

```python
const bot = new lexupload.ImportBot(this, 'lexBot', {
  sourceDirectory: './resources/LexBot',
  lexRoleArn: lexRole.roleArn,
});
```

The `sourceDirecotry` must include a file named `LexBot.zip`. All files in that directory will be uploaded, but only a file named `LexBot.zip` will be imported to Lex as a Bot.

The `lexRoleArn` refers to the roleArn of an IAM Role. For example:

```python
const lexRole = new iam.Role(this, 'lexRole', {
  assumedBy: new iam.ServicePrincipal('lex.amazonaws.com'),
  inlinePolicies: {
    ['lexPolicy']: new iam.PolicyDocument({
      statements: [
        new iam.PolicyStatement({
          resources: ['*'],
          actions: ['polly:SynthesizeSpeech', 'comprehend:DetectSentiment'],
        }),
      ],
    }),
  },
});
```

### Adding a Resource Policy

```python
bot.addResourcePolicy(resourceArn, policy);
```

`addResourcePolicy` requires two properties: the `resourceArn` of the Lex Bot, and a policy to be applied. This policy will be applied to the alias associated with the Bot.

#### Resource ARN Example:

```python
const resourceArn = `arn:aws:lex:${this.region}:${this.account}:bot-alias/${bot.botId}/${bot.botAliasId}`;
```

#### Policy Example:

```python
const policy = {
  Version: '2012-10-17',
  Statement: [
    {
      Sid: 'AllowChimePstnAudioUseBot',
      Effect: 'Allow',
      Principal: { Service: 'voiceconnector.chime.amazonaws.com' },
      Action: 'lex:StartConversation',
      Resource: resourceArn,
      Condition: {
        StringEquals: { 'AWS:SourceAccount': `${this.account}` },
        ArnEquals: {
          'AWS:SourceArn': `arn:aws:voiceconnector:us-east-1:${this.account}:*`,
        },
      },
    },
  ],
};
```

## Not Supported Yet

This is a work in progress.

Features that are not supported yet:

* [ ] Non-Draft Versions
* [ ] Updates to created resources

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
