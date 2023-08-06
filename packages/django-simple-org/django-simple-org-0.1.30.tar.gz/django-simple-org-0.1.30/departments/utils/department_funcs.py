# -*- coding: utf-8 -*-
"""
@File        : department_funcs.py
@Author      : yu wen yang
@Time        : 2022/5/13 10:12 上午
@Description :
"""
import math

from django.db.models import Max
from django.db import transaction

from departments.common.config import BadRequestCode, ServerErrorCode
from departments.models import Department, DepartmentUserMap
from departments.forms.forms import (
    DepartmentForms, MoveDepartmentIndexForms,
)
from departments.utils.error_response import Resp


def get_departments(organization_id: int, department_name: str = None) -> dict:
    """
    通过组织id获取全量部门
    :param organization_id:
    :param department_name:部门名称, 默认为空
    :return:
    """
    # 没有搜索的情况, 直接获取全部
    if not department_name:
        instance = Department.objects.filter(
            organization_id=organization_id,
            path__isnull=True,
            is_deleted=False
        )
        items = list()

        for i in instance:
            items.append(i.department_tree())

    # 有搜索的情况
    else:
        # 查询到包含搜索关键字的部门
        departments = Department.objects.filter(
            organization_id=organization_id,
            name__contains=department_name,
            is_deleted=False
        )
        items = list()
        # 循环每一个部门
        for instance in departments:
            lst = list()
            # 如果有父级的话, 查询到每一个父级部门的内容append到返回列表中
            if instance.path:
                for i in instance.path:
                    dic = {}
                    obj = Department.objects.filter(pk=i).only("name").first()
                    dic["id"] = obj.id
                    dic["name"] = obj.name
                    dic["charger_id"] = obj.charger_id
                    dic["show_order"] = obj.show_order
                    lst.append(dic)
            # 最后把部门本身的内容也append到返回列表中
            lst.append({
                "id": instance.id,
                "name": instance.name,
                "charger_id": instance.charger_id,
                "show_order": instance.show_order
            })
            items.append(lst)

    return Resp(data=items)


def get_sub_department(organization_id: int, department_id=None) -> dict:
    """
    通过部门id获取部门下的子部门, 默认获取所有的一级部门
    :param organization_id: 组织id
    :param department_id: 部门id
    :return:
    """

    if not department_id:
        department_instance = Department.objects.filter(
            organization_id=organization_id, is_deleted=False, path__isnull=True
        )
        department_items = []
        for department in department_instance:
            department_items.append({
                "id": department.id,
                "name": department.name,
                "charger_id": department.charger_id,
                "path": department.path,

            })
        return Resp(data=department_items)

    instance = Department.objects.get(
        pk=department_id,
        organization_id=organization_id,
        is_deleted=False
    )
    department_path = instance.path if instance.path else list()
    department_path.append(department_id)
    department = Department.objects.filter(
        organization_id=organization_id,
        is_deleted=False,
        path=department_path
    )
    return Resp(data=[{"id": i.id, "name": i.name, "charger_id": i.charger_id, "path": i.path} for i in department])


@transaction.atomic
def create_department(data: dict) -> dict:
    """
    新建部门
    :param data:
    :return:
    """

    """
    1. 校验需要创建企业的数据, 判断数据合法性
    2. 构建新建部门path(如果父级部门有path, 将父级部门id加入父级path中;如果父级部门没有path, 则path=父级部门)
    3. 找到数据表中最大的排序数, 将这个数字加1并且创建新的部门.
    """
    # 校验数据
    checked = DepartmentForms(data)
    # 判断数据合法性
    if not checked.is_valid():
        return Resp(code=ServerErrorCode, msg=checked.errors)
    # 构造path
    parent_id = data.pop("parent_id")
    if parent_id:
        parent = Department.objects.get(pk=parent_id)
        if parent.organization_id != data["organization_id"]:
            raise ValueError(
                f"organization_id:{data['organization_id']} different of parent organization_id: {parent.organization_id}")
        if parent.path:
            path = parent.path
            path.append(parent.id)
        else:
            path = [parent.id]
    else:
        if Department.objects.filter(organization_id=data["organization_id"]).exists():
            raise ValueError(f"organization: {data['organization_id']} already has a level-1 department")
        path = []

    # 找到最大排序数
    show_order = Department.objects.aggregate(num=Max('show_order'))["num"]
    data["show_order"] = show_order + 1
    data["path"] = path
    # 查询当前添加的部门同一级别是否有重复
    same_level_department = Department.objects.filter(
        name=data["name"],
        path=path,
        organization_id=data["organization_id"]
    ).exists()

    # 如果当前部门下有这个部门
    if same_level_department:
        return Resp(code=ServerErrorCode, msg=f"[{data['name']}]在当前部门下已存在, 请使用其他名称")

    department_instance = Department.objects.create(**data)
    return Resp(data={'id': department_instance.pk})


def get_department_object(organization_id: int, pk: int):
    """
    获取部门详情
    :param organization_id: 组织id
    :param pk: 部门id
    :return:
    """
    try:
        instance = Department.objects.get(pk=pk, organization_id=organization_id, is_deleted=False)
        return Resp(
            data={
                "id": instance.id,
                "name": instance.name,
                "path": instance.path,
                "charger_id": instance.charger_id,
                "parent_id": instance.path[-1] if instance.path else instance.id,
            }
        )
    except Department.DoesNotExist:
        return Resp(code=ServerErrorCode, msg=f"the department can't be found  id: {pk}")


@transaction.atomic
def update_department(pk: int, data: dict):
    """
    修改部门内容
    :param pk:
    :param data:
    :return:
    """
    checked = DepartmentForms(data)
    # 判断数据合法性
    if not checked.is_valid():
        return Resp(code=ServerErrorCode, msg=checked.errors)
    organization_id = data["organization_id"]
    try:
        instance = Department.objects.get(pk=pk, organization_id=organization_id, is_deleted=False)
        parent_id = data["parent_id"]
        self_path = instance.id

        # 查询当前部门的子级部门(path包含当前部门id的部门)
        son_departments = Department.objects.filter(
            path__contains=[self_path, ]
        ).values_list("id", flat=True)

        # 如果父部门选择了自己或者自己的子级部门抛出异常
        if int(parent_id) == self_path or int(parent_id) in list(son_departments):
            raise ValueError("该父部门不可选择")

        parent = Department.objects.get(organization_id=organization_id, pk=parent_id)
        if parent.path:
            path = parent.path
            path.append(parent.id)
        else:
            path = [parent.id]

        instance.path = path
        instance.name = data["name"]
        instance.charger_id = data["charger_id"]
        instance.save()
        return Resp(data="修改成功")
    except Exception as err:
        raise ValueError(f"{str(err)}  id: {pk}")


@transaction.atomic
def delete_department(organization_id: int, pk: int):
    """
    删除部门
    :param organization_id:
    :param pk:
    :return:
    """
    instance = Department.objects.filter(organization_id=organization_id, pk=pk).first()
    if instance.path:
        path = instance.path
    else:
        raise ValueError("一级部门不允许删除")
    path.append(instance.id)
    dic = {f"path__0_{len(path)}": path}
    departments = list(Department.objects.filter(**dic).values_list("id", flat=True))
    print(departments)
    departments.append(instance.id)
    if DepartmentUserMap.objects.filter(department_id__in=departments).exists():
        raise ValueError("当前部门或子部门下还有用户, 无法删除!")
    Department.objects.filter(id__in=departments).delete()
    return Resp(data="删除成功")


@transaction.atomic
def add_department_user_map(organization_id: int, department_id: int, user_ids: list):
    """
    添加部门-用户的映射关系
    :param organization_id:
    :param department_id:
    :param user_ids:
    :return:
    """
    if not Department.objects.filter(
            organization_id=organization_id, pk=department_id
    ).exists():
        return Resp(code=BadRequestCode, msg="当前组织没有该部门")

    department_user_list = [
        DepartmentUserMap(department_id=department_id, user_id=user) for user in user_ids
    ]
    try:
        DepartmentUserMap.objects.bulk_create(department_user_list)
    except Exception as err:
        raise Exception(err)
    return Resp(data="添加成功")


# def get_department_user(organization_id: int, department_id: int, page: int, size: int):
def get_department_user(organization_id: int, department_ids: list):
    """
    通过部门获取用户
    :param organization_id: 组织id
    :param department_ids: 部门id
    :param page: 页码
    :param size: 每页数量
    :return:
    """
    user_ids = DepartmentUserMap.objects.filter(
        department__organization_id=organization_id,
        department__is_deleted=False,
        department_id__in=department_ids
    ).order_by("-id").values_list("user_id", flat=True)
    return Resp(data=list(user_ids))
    # total = user_ids.count()
    # max_page = math.ceil(total / size)
    # items = [
    #     item for item in user_ids.order_by("-id").values_list("user_id", flat=True)[(page-1)*size: page*size]
    # ] if page <= max_page else []
    #
    # return Resp(data={
    #     "total": total,
    #     "page_range": [i for i in range(1, max_page+1)],
    #     "current_page": page,
    #     "list": items
    # })


@transaction.atomic
def delete_department_user_map(organization_id: int, department_id: int, user_ids: list):
    """
    添加部门-用户的映射关系
    :param organization_id:
    :param department_id:
    :param user_ids:
    :return:
    """
    if not Department.objects.filter(
            organization_id=organization_id, pk=department_id
    ).exists():
        return Resp(code=BadRequestCode, msg="当前组织没有该部门")

    DepartmentUserMap.objects.filter(
        department__organization_id=organization_id,
        user_id__in=user_ids
    ).delete()

    return Resp(data="移除成功")


def mv_show_order(organization_id: int, data: dict):
    """
    修改部门show_order
    :param organization_id:  组织id
    :param data:  {"department_id": 1, "type": "up"}
    :return:
    """
    """
    查询修改的部门, 拿到path, 查询所有path相同的部门
    """
    checked = MoveDepartmentIndexForms(data)
    if not checked.is_valid():
        return Resp(code=ServerErrorCode, msg=checked.errors)
    try:
        instance = Department.objects.get(pk=data["department_id"], organization_id=organization_id)
    except Department.DoesNotExist:
        return Resp(code=ServerErrorCode, msg=f"the organization:{organization_id} not found department_id: {data['department_id']}")
    path = instance.path
    departments = list(Department.objects.filter(
        path=path, organization_id=organization_id
    ).values_list("id", flat=True))
    instance_index = departments.index(instance.id)

    # 判断移动类型
    if data["type"] == "up":
        index = instance_index - 1
    elif data["type"] == "down":
        index = instance_index + 1
    else:
        return Resp(code=BadRequestCode, msg=f"failed type [{data['type']}]")

    # 修改后的下标最大不可以超过列表长度  最小不可以小于0
    if (len(departments) - 1) < index or index < 0:
        return Resp(code=BadRequestCode, msg="index error")
    moved_department = Department.objects.get(pk=departments[index], organization_id=organization_id)
    instance_show_order = instance.show_order
    moved_department_show_order = moved_department.show_order
    instance.show_order = moved_department_show_order
    moved_department.show_order = instance_show_order
    instance.save()
    moved_department.save()

    return Resp()


def get_all_chargers(organization_id: int):
    return Resp(data=list(DepartmentUserMap.objects.filter(
        department__organization_id=organization_id,
    ).order_by("user_id").values_list("user_id", flat=True)))


def get_organization_users(organization_id: int):
    """
    获取组织下所有的用户
    :param organization_id:
    :return:
    """
    user_ids = DepartmentUserMap.objects.filter(
        department__organization_id=organization_id
    ).values_list("user_id", flat=True)
    return Resp(data=list(user_ids))


def exclude_department_users(organization_id: int, department_id: int):
    """
    获取企业中除了这个部门中用户的其他用户
    :param organization_id:
    :param department_id:
    :return:
    """
    organization_users = get_organization_users(organization_id)
    if not organization_users["code"] == 200:
        return Resp(code=ServerErrorCode, msg=f"{organization_users['msg']}")
    department_users = get_department_user(organization_id, department_id)
    if not department_users["code"] == 200:
        return Resp(code=ServerErrorCode, msg=f"{department_users['msg']}")

    all_users = set(organization_users["data"])
    excluded_users = set(department_users["data"])
    if not excluded_users.issubset(all_users):
        return Resp(code=ServerErrorCode, msg=f"excluded users aren't subset of all users")
    users = all_users.difference(excluded_users)
    return Resp(data=list(users))


@transaction.atomic
def user_change_department(organization_id: int, user_id: int, department_ids: list):
    """
    用户变更部门
    :param organization_id:
    :param user_id:
    :param department_ids:
    :return:
    """
    try:
        DepartmentUserMap.objects.filter(
            department__organization_id=organization_id,
            user_id=user_id
        ).delete()

        changed_instance_list = [DepartmentUserMap(department_id=id_, user_id=user_id) for id_ in department_ids]
        DepartmentUserMap.objects.bulk_create(changed_instance_list)
        return Resp()
    except Exception as e:
        raise Exception(str(e))


def get_user_departments(organization_id: int, user_id: int):
    """
    获取用户所在的部门
    :param organization_id:
    :param user_id:
    :return:
    """
    user_departments = DepartmentUserMap.objects.filter(
        department__organization_id=organization_id,
        user_id=user_id
    ).values_list("department_id", flat=True)

    return Resp(data=list(user_departments))

