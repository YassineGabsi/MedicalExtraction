import {environment} from '../../environments/environment';

export class Utils {

  public static baseUrl = environment.production ?
  'http://medical-extraction.eu-central-1.elasticbeanstalk.com' : 'http://medical-extraction.eu-central-1.elasticbeanstalk.com';

  public static url = Utils.baseUrl + '/api/';
}
