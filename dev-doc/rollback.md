# Rollback Plan

## Quick Rollback Procedure

1. **Trigger quick rollback** to previous stable image via deployment system
2. **If DB migration applied**, apply compensating migration or restore DB from snapshot
3. **Notify stakeholders** and open incident ticket
4. **Run post-rollback verification tests**

## Solo-Dev Rollback

### Image Rollback

1. Identify previous stable version/tag
2. Revert deployment to previous version
3. Verify application works

### Database Rollback

1. If migration applied, check if reversible
2. Apply rollback migration if available
3. Or restore from backup snapshot
4. Verify data integrity

### Post-Rollback

1. Run smoke tests
2. Verify critical functionality
3. Document what went wrong
4. Create issue for fix

## Rollback Decision Matrix

- **Critical bug affecting users** → Immediate rollback
- **Performance degradation** → Monitor, rollback if severe
- **Minor issues** → Hotfix instead of rollback


