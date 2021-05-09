import {environment} from '../../environments/environment';

export class Utils {

  public static baseUrl = environment.production ?
    'http://medical-extraction.eu-central-1.elasticbeanstalk.com' : 'http://medical-extraction.eu-central-1.elasticbeanstalk.com';

  public static url = Utils.baseUrl + '/api/';

  public static validateEmail(email) {
    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    return re.test(String(email).toLowerCase());
  }
}
