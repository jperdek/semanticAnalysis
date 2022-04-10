export const environment = {
  debug: false,
  useOcta: true,
  production: true,
  apiBaseUrl: 'https://semanticaspectsapp.azurewebsites.net',
  octa_data: {
    client_id: '0oa19wfjhrBoVLqSw5d7',
    issuer: 'https://dev-03853854.okta.com',
    login_redirect_uri: 'https://semanticaspectsfrontend.azurewebsites.net/lcallback',
    logout_redirect_uri: 'https://semanticaspectsfrontend.azurewebsites.net/',
    register_address: 'https://dev-03853854.okta.com/api/v1/users?activate=true',
    ssws_api_token: '00LILaDwqgSXxJl2UTwZzLEIRybFy2j3RdtSwrt7uW'
  }
};
