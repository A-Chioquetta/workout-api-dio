from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaListOut, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DataBaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    categoria_name = atleta_in.categoria.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria não encontrada: {categoria_name}",
        )

    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Centro de Treinamento não encontrado: {centro_treinamento_nome}",
        )

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id

    db_session.add(atleta_model)

    try:
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )
    return atleta_out


@router.get(
    "/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaListOut],
)
async def query(
    db_session: DataBaseDependency,
) -> LimitOffsetPage[AtletaListOut]:
    stmt = select(AtletaModel)
    return await paginate(db_session, stmt)


@router.get(
    "/search",
    summary="Buscar atleta por ID ou CPF",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def buscar_atleta(
    db_session: DataBaseDependency,
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> AtletaOut:

    if not id and not cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe id ou cpf.",
        )

    if id and cpf:
        stmt = select(AtletaModel).filter_by(id=id, cpf=cpf)
        atleta = (await db_session.execute(stmt)).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID e CPF informados não pertencem ao mesmo atleta.",
            )

        return AtletaOut.model_validate(atleta)

    if id:
        stmt = select(AtletaModel).filter_by(id=id)

    else:
        stmt = select(AtletaModel).filter_by(cpf=cpf)

    atleta = (await db_session.execute(stmt)).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado.",
        )

    return AtletaOut.model_validate(atleta)


@router.patch(
    "/{id}",
    summary="Editar um atleta pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado para o id: {id}",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    "/{id}",
    summary="Deletar um atleta pelo ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def get(
    id: UUID4,
    db_session: DataBaseDependency,
) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado para o id: {id}",
        )

    await db_session.delete(atleta)
    await db_session.commit()
