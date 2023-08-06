from ...models.assets import UnstructuredInputAsset
import pytest


class TestUnstructuredInputAsset:
    def test_asset_valid(self):
        asset = UnstructuredInputAsset(
            uri="s3://some_uri",
            sensor="camera_back"
        )
        assert asset.uri == "s3://some_uri"
        assert asset.sensor == "camera_back"
        # timestamp always exists
        assert asset.timestamp

    def test_asset_invalid(self):
        with pytest.raises(AssertionError) as e:
            asset = UnstructuredInputAsset(
                uri="s3://some_uri",
                url="http://some_uri",
                sensor="camera_back"
            )

    def test_asset_standardize_id(self):
        asset = UnstructuredInputAsset(
            id="sOmE id . ~",
            uri="s3://some_uri",
            sensor="camera_back"
        )

        assert asset.id == "some_id_._~"



