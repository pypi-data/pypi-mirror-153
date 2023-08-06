// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { TableModel } from '..';

describe('TableView', () => {
  describe('TableModel', () => {
    it('should be createable', () => {
      const model = createTestModel(TableModel);
      expect(model).toBeInstanceOf(TableModel);
      expect(model.get('selected')).toEqual(-1);
    });
  });
});
