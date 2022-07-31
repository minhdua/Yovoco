// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  firebase: {
    projectId: 'test-55635',
    appId: '1:588001937074:web:9c72bc4bf678c9546eabab',
    storageBucket: 'test-55635.appspot.com',
    locationId: 'us-central',
    apiKey: 'AIzaSyCg9NPb8UKnTrhBsl8137lGGWpTfA4vdPE',
    authDomain: 'test-55635.firebaseapp.com',
    messagingSenderId: '588001937074',
    measurementId: 'G-55Q7N120MB',
  },
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
