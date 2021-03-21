import {environment} from '../../environments/environment';

export class Utils {

  public static baseUrl = environment.production ?
  'http://localhost:4200' : 'http://localhost:4200';

  public static url = Utils.baseUrl + '/api/';


}
