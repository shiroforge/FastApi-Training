from sqlalchemy.orm import Session
from app.models.models import User

# ユーザー作成
# 引数としてusernameとemailを受け取り、新しいユーザーをデータベースに追加する。
def create_user(db: Session, username: str, email: str) -> User:
    # 引数で渡された情報をもとに、新しいUserオブジェクトを格納する。
    new_user = User(username=username, email=email)
    # データベース(テーブル）に追加を行う
    db.add(new_user)
    # コミットする
    db.commit()
    # リフレッシュする
    db.refresh(new_user)
    # 作成したユーザーを返す
    return new_user

# 全ユーザーを取得
def get_users(db: Session):
    # データベースから全てのユーザーを取得して返す
    return db.query(User).all()

# 特定のユーザーを取得
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# ユーザー情報更新
# 引数としてuser_id、username、emailを受け取り、該当するユーザーの情報を更新する。
# SQLAlchemyは「取得したオブジェクトの属性を書き換えてcommitするだけ」で自動的にUPDATE文を発行してくれるため、明示的なSQLを書く必要がありません。
def update_user(db: Session, user_id: int, username: str = None, email: str = None) -> User:
    # ユーザーを取得
    user = db.query(User).filter(User.id == user_id).first()
    # ユーザーが見つからない場合はNoneを返す
    if not user:
        return None  # ユーザーが見つからない場合はNoneを返す
    # 更新するフィールドが指定されている場合のみ更新
    if username:
        user.username = username
    # emailが指定されている場合のみ更新
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user

# ユーザー情報削除
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False  # ユーザーが見つからない場合はFalseを返す
    db.delete(user)
    db.commit()
    return True