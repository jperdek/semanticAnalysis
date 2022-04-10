// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  debug: true,
  useOcta: true,
  production: false,
  apiBaseUrl: 'http://localhost:5000',
  octa_data: {
    client_id: '0oa19wfjhrBoVLqSw5d7',
    issuer: 'https://dev-03853854.okta.com',
    login_redirect_uri: 'http://localhost:4200/lcallback',
    logout_redirect_uri: 'http://localhost:4200/',
    register_address: 'https://dev-03853854.okta.com/api/v1/users?activate=true',
    ssws_api_token: '00LILaDwqgSXxJl2UTwZzLEIRybFy2j3RdtSwrt7uW'
  }
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
