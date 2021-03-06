import { authClient } from 'infras/RestClient';
import { TermFactory, TermObject } from 'domains';

interface TermCreateRequest {
  academicYear: number;
  semester: string;
}

export interface TermInterface {
  academic_year: number;
  semester: string;
  uuid: string;
}

export class TermRepository {
  static async gets(year: number, semester: string) {
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.get<TermInterface[]>(
      `/api/v1/terms/?academic_year=${year}&semester=${semester}`,
    );
    //return res.data.map(term => TermFactory.createFromResponseObject(term));
    return res.data;
  }
  static async get(uuid: string) {
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.get<TermObject>(`/api/v1/terms/${uuid}`);
    return TermFactory.createFromResponseObject(res.data);
  }
  public static async create({ academicYear, semester }: TermCreateRequest) {
    const params = {
      academicYear,
      semester,
    };
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.post<TermCreateRequest, TermObject>(
      `/api/v1/terms`,
      params,
    );
    return TermFactory.createFromResponseObject(res.data);
  }
}
