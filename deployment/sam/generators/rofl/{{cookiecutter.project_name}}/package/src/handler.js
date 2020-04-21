const rofl = require('@narrativescience/rofl').default

 // TODO(QPT-22479): enable pulling secrets from SecretsManager
// const { getSecrets } = require('./secrets')

module.exports.handler = async (event, context) => {
  // TODO(QPT-22479): enable pulling secrets from SecretsManager
  // try {
  //   const secrets = await getSecrets(
  //     `${process.env.Environment}/${process.env.Platform}/${
  //       process.env.Function
  //     }`
  //   )
  //
  // } catch (err) {
  //   console.error(err)
  //   return {
  //     statusCode: err.statusCode || 500,
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(err.body ? err.body : err)
  //   }
  // }

  try {
    const response = await rofl('./rofl.yml', event)
    return response
  } catch (err) {
    console.error(err)
    return {
      statusCode: err.statusCode || 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(err.body ? err.body : err)
    }
  }
}
