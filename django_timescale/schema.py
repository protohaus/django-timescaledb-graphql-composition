from graphene import relay, ObjectType, Schema
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from farms.models import (
    Site,
    SiteEntity,
    ControllerComponent,
    PeripheralComponent,
    PoseComponent,
    DataPointType,
    DataPoint,
)


class SiteNode(DjangoObjectType):
    class Meta:
        model = Site
        filter_fields = {"name": ["exact", "icontains", "istartswith"]}
        interfaces = (relay.Node,)


class SiteElementNode(DjangoObjectType):
    class Meta:
        model = SiteEntity
        filter_fields = ["site", "name"]
        interfaces = (relay.Node,)


class ControllerComponentNode(DjangoObjectType):
    class Meta:
        model = ControllerComponent
        filter_fields = {"site_entity": ["exact"], "created_at": ["exact", "lt", "gt"]}
        interfaces = (relay.Node,)


class PeripheralComponentNode(DjangoObjectType):
    class Meta:
        model = PeripheralComponent
        filter_fields = {
            "site_entity": ["exact"],
            "site_entity__site": ["exact"],
            "controller_component": ["exact"],
            "config": [],
        }
        interfaces = (relay.Node,)


class PoseComponentNode(DjangoObjectType):
    class Meta:
        model = PoseComponent
        filter_fields = ["site_entity", "relative_to", "x", "y", "z"]
        interfaces = (relay.Node,)


class DataPointTypeNode(DjangoObjectType):
    class Meta:
        model = DataPointType
        filter_fields = ["name", "unit"]
        interfaces = (relay.Node,)

class DataPointNode(DjangoObjectType):
    class Meta:
        model = DataPoint
        filter_fields = {
            "time": ["exact", "lt", "gt"],
            "peripheral": ["exact"],
            "data_type": ["exact"],
            "value": ["exact", "lt", "gt"],
        }
        interfaces = (relay.Node,)

class Query(ObjectType):
    site = relay.Node.Field(SiteNode)
    all_sites = DjangoFilterConnectionField(SiteNode)

    site_element = relay.Node.Field(SiteElementNode)
    all_site_elements = DjangoFilterConnectionField(SiteElementNode)

    controller_component = relay.Node.Field(ControllerComponentNode)
    all_controller_components = DjangoFilterConnectionField(ControllerComponentNode)

    peripheral_component = relay.Node.Field(PeripheralComponentNode)
    all_peripheral_components = DjangoFilterConnectionField(PeripheralComponentNode)

    pose_component = relay.Node.Field(PoseComponentNode)
    all_pose_components = DjangoFilterConnectionField(PoseComponentNode)

    data_point_type = relay.Node.Field(DataPointTypeNode)
    all_data_point_types = DjangoFilterConnectionField(DataPointTypeNode)

    data_point = relay.Node.Field(DataPointTypeNode)
    all_data_points = DjangoFilterConnectionField(DataPointNode)


schema = Schema(query=Query)