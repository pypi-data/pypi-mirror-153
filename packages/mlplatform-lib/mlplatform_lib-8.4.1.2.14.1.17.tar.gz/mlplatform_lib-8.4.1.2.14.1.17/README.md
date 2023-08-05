## Hyperdata Library

## 폴더 트리 구조

![Folder Tree Architecture](folder.png "Folder Tree Architecture")

위 이미지는 PredefinedAI에서 사용하는 폴더 트리 구조입니다.

- 실험 별 경로는 ${mount_path}/${experiment_id}
- 버전 별 경로는 ${mount_path}/${experiment_id}/\${workflow_id}
- 추론 별 경로는 ${mount_path}/${experiment_id}/${workflow_id}/${inference_id}

## Prerequisites

내부적으로 모든 함수는 입력받는 파라미터가 없으며, 환경변수 값을 통해 수행됩니다.

AutoML 서버를 통해 수행할 때, 해당 환경변수들은 내부적으로 모두 제공됩니다.

로컬테스트 시, 아래 환경변수들은 제공되어야 합니다.

| Envs           | Description                                                                   |
| -------------- | ----------------------------------------------------------------------------- |
| hyperdata_addr | hyperdata 주소(ex. http://127.0.0.1:8080)                                     |
| project_id     | 테스트할 hyperdata의 project id(ex. 1)                                        |
| user_id        | 테스트할 hyperdata의 user id(ex. admin)                                       |  |
| token          | 테스트할 hyperdata의 user 소유의 토큰                                         |
| mount_path     | 쿠버네티스의 pvc가 마운트된 경로. 로컬테스트 시 로컬 파일시스템의 경로를 사용 |
| experiment_id  | 실험 id                                                                       |
| workflow_id    | 버전 id                                                                       |
| inference_id   | 추론 id                                                                       |
| do_id          | 현재 사용할 do의 id                                                           |

## API List

### hyperdata_api

| API                     | Description                                                                   |
| ----------------------- | ----------------------------------------------------------------------------- |
| get_experiment_path     | 현 실험 경로                                                                  |
| get_workflow_path       | 현 버전 경로                                                                  |
| get_prev_workflow_paths | 이전 버전들 경로 리스트                                                       |
| get_inference_path      | 현 추론 경로                                                                  |
| download_train_csv      | do id 기반으로 dataobject를 csv로 다운로드 및 다운로드 받아진 csv의 경로 리턴 |
| download_retrain_csv    | do id 기반으로 dataobject를 csv로 다운로드 및 다운로드 받아진 csv의 경로 리턴 |
| download_inference_csv  | do id 기반으로 dataobject를 csv로 다운로드 및 다운로드 받아진 csv의 경로 리턴 |
| get_workflow_id         | 현 버전 id                                                                    |
| get_inference_id        | 현 추론 id                                                                    |

### predefinedai_api

| API                    | Description                         |
| ---------------------- | ----------------------------------- |
| get_model_infos        | 현재 실험의 model 정보 리스트       |
| insert_model_info      | 현 버전에 model 정보 삽입           |
| insert_visualizations  | 현 버전에 시각화 정보 삽입          |
| get_inference_csv_path | 현 추론 데이터를 저장해야 하는 경로 |
| upload_inference_csv   | 서버로 추론 데이터 업로드           |

### predefinedai_template_test

| API | Description |
| --- | ----------- |
| run | 테스트 수행 |
