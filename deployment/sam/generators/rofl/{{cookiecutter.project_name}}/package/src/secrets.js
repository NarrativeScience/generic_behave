const AWS = require('aws-sdk')

const secretsManager = new AWS.SecretsManager({
  region: process.env.AWS_DEFAULT_REGION
})

export const getSecrets = async key => {
  const data = await secretsManager
    .getSecretValue({
      SecretId: key
    })
    .promise()
  // Decrypts secret using the associated KMS CMK. Depending on whether the secret is a
  // string or binary, one of these fields will be populated.
  let secrets
  if ('SecretString' in data) {
    secrets = JSON.parse(data.SecretString)
  } else {
    const buff = new Buffer(data.SecretBinary, 'base64')
    secrets = JSON.parse(buff.toString('ascii'))
  }
  return secrets
}
