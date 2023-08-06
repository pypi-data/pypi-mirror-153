# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains core concept classes which strictly align with SDK 2.0 design.

See https://github.com/Azure/azureml_run_specification/blob/master/concepts.md
"""


class Base(object):

    @property
    def name(self):
        """name of the resource"""
        pass

    @property
    def type(self):
        """
        the type of the object.

        It is used to identify the schema if the object is inlined into another object.
        """
        pass

    @property
    def schema(self):
        """
        refers to the schema that this object adheres to.

        It is only needed if the object is serialized into a separate file"""
        pass

    @property
    def identifier(self):
        """identifier of the resource"""
        pass

    @property
    def metadata(self):
        pass

    @property
    def description(self):
        """A description of the resource"""
        pass

    @property
    def tags(self):
        """name-value pairs which manifest as properties of the tags object"""
        pass

    @property
    def creation_context(self):
        """creation_context with user and time as well as modification_time"""
        pass

    @property
    def workspace(self):
        """workspace which the resource belongs to"""
        pass


class AssetVersion(Base):
    """
    An asset can be registered to the workspace which contain one or more versions.

    Each version also has its own associated metadata.
    An assetversion has the following:
        - name
        - identifier
        - description
        - tags
            - including a namespace tag

    In addition, each distinct assetversion version has the following:
        - version
        - label
        - versionDescription
        - versionTags

    Default version:
        Each assetversion has a default version. By default, the default version is set to the latest version.
        Users can override this by setting their own default version of the assetversion.

    Anonymous assetversions:
        “Anonymous” assetversions are unregistered assetversions that show up in the workspace,
        e.g. as part of Component/Pipeline runs, with only an assetversion ID.
        User can register the anonymous assetversion from the UI.
    """
    @property
    def version(self):
        """
        identifier of type string.

        This is never mutable, no constraints about what the version string looks like.
        The only constraint is that the version is unique to the object (there can only be one version "1").
        """
        raise NotImplementedError

    @property
    def labels(self):
        """
        an array of string.

        A label is an alias for that version, allows users to track concepts like "beta" or "stable" that points
        to different versions at different times. For some or all objects, we will keep a 'latest' label that will
        automatically point to the latest version of the object.
        """
        raise NotImplementedError

    @property
    def versionDescription(self):
        raise NotImplementedError

    @property
    def versionTags(self):
        """key-with-optional-value pairs used for organization.

        like applying a "validatedByManualTest" tag to every component someone tested.
        """
        raise NotImplementedError

    @property
    def modification_time(self):
        raise NotImplementedError

    def register(self):
        """Register an in-memory object created from SDK to the workspace.

        Registering associates an assetversion with the workspace assetversion registry.
        """
        raise NotImplementedError

    def save(self):
        """Save out the yaml specification for an assetversion to disk."""
        raise NotImplementedError

    @staticmethod
    def load(self):
        """Instantiate an assetversion object from the yaml specification."""
        raise NotImplementedError

    @staticmethod
    def get(self):
        """Retrieve a registered assetversion from the workspace.

        If version is not specified, the default version will be returned.
        """
        raise NotImplementedError

    @staticmethod
    def list(self):
        """Return all assetversions registered to the workspace.

        By default archived assetversions will not be returned.
        """
        raise NotImplementedError

    def set_as_default(self):
        """Set a given assetversion version as the default version for the assetversion."""
        raise NotImplementedError

    def archive(self):
        """
        Archive an assetversion.

        Archived assetversions will be hidden from queries by default (e.g. in the UI, SDK calls such as list()).
        """
        raise NotImplementedError

    def restore(self):
        """
        Restore an archived assetversion.
        """
        raise NotImplementedError

    def delete(self):
        """
        Permanently delete an assetversion.

        Azure ML will throw an error if user tries to delete an assetversion that is being used.
        In general, assetversion deletion should be used sparingly & deliberately.
        For reproducibility/auditing/lineage purposes, users should archive instead.
        """
        raise NotImplementedError

    def update(self):
        """Update the metadata for an assetversion."""
        raise NotImplementedError

    def archive_all_versions(self):
        """Archive all versions of an assetversion."""
        raise NotImplementedError

    def resotre_all_versions(self):
        """Restore all versions of an assetversion."""
        raise NotImplementedError

    def delete_all_versions(self):
        """Permanently delete all versions of an assetversion."""
        raise NotImplementedError


class Component(AssetVersion):
    """A Component captures a program which can be a step of a pipeline.

    In the abstract, a component only has inputs and outputs.
    """
    @property
    def inputs(self):
        raise NotImplementedError

    @property
    def outputs(self):
        raise NotImplementedError

    def run(self):
        """
        run this component
        """
        raise NotImplementedError


class Resource(Base):
    @property
    def modification_time(self):
        raise NotImplementedError


class Job(Resource):
    """A Job is a Resource that specifies all aspects of a computation job."""
    def __init__(self):
        pass

    @property
    def inputs(self):
        """the inputs which the Component should be configured."""
        pass

    @property
    def outputs(self):
        """the outputs."""
        pass

    @property
    def component(self) -> 'Component':
        """
        A Component that this job is to be executed
        """
        pass

    @property
    def target(self):
        """The Compute on which the job should be executed."""
        pass
