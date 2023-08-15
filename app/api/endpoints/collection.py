from fastapi import APIRouter, Depends

from app.types.jwt import Role
from app.auth.jwt import RequireRole
from app.db.connection import MySqlSession
from app.models.mysql import User, Collection, UserWatchlist

from app.types.eth import EthAddress
from app.types.server import ServerResponse

router = APIRouter(prefix='/collection')


@router.get('/{address}')
async def get_collection(address: str) -> ServerResponse[str]:
    return ServerResponse(data=address)


@router.get('/favorite/{collectionAddress}')
async def favoriteCollection(collectionAddress: EthAddress,
                             user: User = Depends(RequireRole(Role.USER))) -> ServerResponse[str]:
    session = MySqlSession()

    collection = session.query(Collection).filter(
        Collection.address == collectionAddress).one()
    userWatchlist = UserWatchlist(userID=user.id, collectionID=collection.id)

    session.add(userWatchlist)
    session.commit()

    return ServerResponse()


@router.get('/unfavorite/{collectionAddress}')
async def unfavoriteCollection(collectionAddress: EthAddress,
                               user: User = Depends(RequireRole(Role.USER))) -> ServerResponse[str]:
    session = MySqlSession()
    collectionID = session.query(Collection).filter(
        Collection.address == collectionAddress).one()

    session.query(UserWatchlist).filter(
        UserWatchlist.userID == user.id,
        UserWatchlist.collectionID == collectionID.id).delete()
    session.commit()

    return ServerResponse()
