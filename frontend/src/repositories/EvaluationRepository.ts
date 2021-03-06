import { authClient } from 'infras/RestClient';
import {
  EvaluationFactory,
  EvaluationObject,
  Evaluation,
  Subject,
} from 'domains';

interface EvaluationCreateRequest {
  subject: Subject;
  name: string;
  rate: number;
  type: string;
}

interface EvaluationUpdateRequest {
  uuid: string;
  subject: Subject;
  name: string;
  rate: number;
  type: string;
}

export class EvaluationRepository {
  static async gets(subjectUuid: string) {
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.get<EvaluationObject[]>(
      `/api/v1/evaluations?subject_uuid=${subjectUuid}`,
    );
    return res.data.map(evaluation =>
      EvaluationFactory.createFromResponseObject(evaluation),
    );
  }
  static async get(uuid: string) {
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.get<EvaluationObject>(
      `/api/v1/evaluations/${uuid}`,
    );
    return EvaluationFactory.createFromResponseObject(res.data);
  }

  public static async create({
    subject,
    name,
    rate,
    type,
  }: EvaluationCreateRequest) {
    const params = {
      subject,
      name,
      rate,
      type,
    };
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.post<
      EvaluationCreateRequest,
      Evaluation
    >(`/api/v1/evaluations`, params);
    return res.data;
  }

  public static async update({
    uuid,
    subject,
    name,
    rate,
    type,
  }: Partial<EvaluationUpdateRequest>) {
    const params = {
      uuid,
      subject,
      name,
      rate,
      type,
    };
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.put<
      Partial<EvaluationUpdateRequest>,
      EvaluationObject
    >('/api/v1/evaluations', params);
    return EvaluationFactory.createFromResponseObject(res.data);
  }

  public static async delete(uuid: string) {
    const authClientObject = authClient();
    if (!authClientObject) return;
    const res = await authClientObject.delete(`api/v1/evaluations/${uuid}`);
    return res.data.text;
  }
}
