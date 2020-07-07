# 01. python - django

## 1-1. django 초기 설정

#### 1-1-1가상환경 만들기

- `pip install -r requirement.txt`구문을 실행하기 전에 가상환경을 만들고 실행해야 합니다.

  - 가상환경을 만들어서 해야 하는 이유는 파이썬 가상환경 구글링 하면 이유가 나옵니다. 

- 터미널 창에서 deckend 폴더 내에서 `python -m venv venv`를 입력해서 가상환경 파일을 만들어 줍니다. git에 commit 할 때는 `.gitignore`때문에 올라가지 않습니다. (각자 만들어줘야해요)

- 한번 만들면 파일을 새로 `clone`하는 경우가 아니면 입력할 필요 없어요

- ```bash
  multicampus@DESKTOP-KVCQHCD MINGW64 ~/Desktop/s02p22b206/sub2/backend
  $ python -m venv venv
  ```

#### 1-1-2 가상환경 실행

- 가상환경 실행하는 방법은  터미널 창에서 진행 합니다. 

- `source venv/Scripts/activate`를 입력합니다.

  - vscode를 껐다가 키면 가상환경이 꺼져있을꺼에요. 프로젝트 진행할 때마다 가상환경을 켜줘야합니다. 

- 제대로 실행되면 터미널 하단에 `(venv)` 가 뜹니다.

  ```bash
  multicampus@DESKTOP-KVCQHCD MINGW64 ~/Desktop/s02p22b206/sub2/backend (dev/feature/woo)
  $ source venv/Scripts/activate
  (venv)
  ```

#### 1-1-3 pip install

- sub2에서는 친절하게 `requirements.txt`가 있어서 쉽습니다.
- 가상환경이 켜져 있는 상황에서 `pip install -r requirement.txt`실행합니다. 
- 개발하다보면 추가적으로 깔아줘야하는 라이브러리등이 필요할 수 있는데 새로 설치를 했다면 
- `pip freeze > requirements.txt`를 통해서 가상환경에 설치돼 있는 패키지들을 저장할 수 있음
- 이렇게 해줘야 여러명이서 프로젝트 진행 할때 필요 패키지들을 쉽게 설치 가능 합니다.

## 1-2. django 실행.

- 터미널창에서 backend 폴더까지 경로이동하고

- ```bash
  $ python manage.py runserver
  ```

- 를 입력하면 서버가 켜집니다. 안켜진다면 가상환경이 켜져있는지 확인해보세요.

```bash
multicampus@DESKTOP-KVCQHCD MINGW64 ~/Desktop/s02p22b206/sub2/backend (dev/feature/woo)
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
April 01, 2020 - 15:30:00
Django version 2.2.7, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
```

