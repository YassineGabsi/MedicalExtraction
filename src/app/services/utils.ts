import {environment} from '../../environments/environment';

export class Utils {

  public static baseUrl = environment.production ?
  'http://localhost:8000' : 'http://localhost:8000';

  public static url = Utils.baseUrl + '/api/';


}
